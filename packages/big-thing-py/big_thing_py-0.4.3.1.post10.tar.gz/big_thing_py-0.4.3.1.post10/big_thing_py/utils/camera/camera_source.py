__all__ = ['CameraSource', 'USBCameraSource', 'RTSPStream', 'ONVIFSource', 'IPCameraSource', 'PiCameraSource']

import asyncio
import os, subprocess
from typing import List, Union
from typing_extensions import override
from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from big_thing_py.utils import is_raspberry_pi

import cv2
import numpy as np
from onvif import ONVIFCamera
from termcolor import cprint


if is_raspberry_pi():
    try:
        from picamera2 import Picamera2
        from picamera2.encoders import H264Encoder
    except ImportError:
        cprint('Picamera2 모듈을 import할 수 없습니다. 라즈베리파이에 올바르게 설치되어 있는지 확인하세요.', 'yellow')
else:
    cprint('이 시스템은 라즈베리파이가 아닙니다. Picamera2를 사용할 수 없습니다.', 'yellow')


class CameraSource(metaclass=ABCMeta):
    def __init__(
        self,
        resolution: tuple[int, int] = (1280, 960),
        fps: int = 60,
    ):
        self._resolution = resolution
        self._fps = fps
        self._cap: cv2.VideoCapture = None
        self._is_cam_on = False
        self._current_frame: Union[None, np.ndarray] = None
        # self._capture_frame_task: asyncio.Task = None

    async def init(self) -> None:
        self.cam_on()
        self.cam_off()

        # self._capture_frame_task = asyncio.create_task(self.capture_frame_task())
        await asyncio.sleep(0)
        cprint('Camera source initialized.', 'green')

    async def teardown(self) -> None:
        self.cam_off()

        # if self._capture_frame_task:
        #     self._capture_frame_task.cancel()
        #     try:
        #         await self._capture_frame_task
        #     except asyncio.CancelledError:
        #         pass

        cprint('Camera source teardown.', 'yellow')

    # async def capture_frame_task(self) -> None:
    #     while True:
    #         if self._cam_on and self._cap:
    #             ret, frame = self._cap.read()
    #             if ret:
    #                 self._current_frame = frame
    #         await asyncio.sleep(1 / self._fps)

    @abstractmethod
    def cam_on(self) -> None: ...

    @abstractmethod
    def cam_off(self) -> None: ...

    @property
    def resolution(self) -> tuple[int, int]:
        return self._resolution

    @property
    def fps(self) -> int:
        return self._fps

    @property
    def is_cam_on(self) -> bool:
        return self._is_cam_on

    @resolution.setter
    def resolution(self, resolution: tuple[int, int]) -> None:
        self._resolution = resolution
        self._cap.set(cv2.CAP_PROP_FRAME_WIDTH, resolution[0])
        self._cap.set(cv2.CAP_PROP_FRAME_HEIGHT, resolution[1])

    @fps.setter
    def fps(self, fps: int) -> None:
        self._fps = fps
        self._cap.set(cv2.CAP_PROP_FPS, fps)

    @property
    def current_frame(self) -> Union[None, np.ndarray]:
        ret, frame = self._cap.read()
        if ret:
            self._current_frame = frame
        else:
            cprint('Cannot read frame from camera.', 'red')
        return self._current_frame


class USBCameraSource(CameraSource):

    def __init__(
        self,
        device_num: int = 0,
        resolution: tuple[int, int] = (640, 480),
        fps: int = 60,
        auto_detect: bool = False,
    ) -> None:
        super().__init__(resolution=resolution, fps=fps)

        self._device_num = device_num
        self._resoultion = resolution
        self._fps = fps

        self._auto_detect = auto_detect
        self._last_camera_index: int = None

    @override
    def cam_on(self) -> None:
        if self._cap is None:
            if self._last_camera_index:
                self._cap = cv2.VideoCapture(self._last_camera_index)
            elif self._auto_detect:
                index = self._get_usb_camera()
                self._cap = cv2.VideoCapture(index)
                self._last_camera_index = index
            else:
                self._cap = cv2.VideoCapture(self._device_num)
                self._last_camera_index = self._device_num

            if not self._cap.isOpened():
                raise ValueError(f'Cannot open camera at index {self._last_camera_index}')

            self._cap.set(cv2.CAP_PROP_FRAME_WIDTH, self._resoultion[0])
            self._cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self._resoultion[1])
        else:
            cprint('Camera is already on.', 'yellow')

        self._cam_on = True

    @override
    def cam_off(self) -> None:
        if self._cap is not None:
            self._cap.release()
            self._cap = None
        else:
            cprint('Camera is already off.', 'yellow')

        self._cam_on = False

    def _get_usb_camera(self) -> int:
        camera_indices = []
        try:
            result = subprocess.run(['v4l2-ctl', '--list-devices'], capture_output=True, text=True, check=True)
            devices = result.stdout.split('\n')

            for i, line in enumerate(devices):
                if 'usb' in line.lower():
                    if i + 1 < len(devices):
                        device_path = devices[i + 1].strip()
                        if '/dev/video' in device_path:
                            index = int(device_path.replace('/dev/video', ''))
                            camera_indices.append(index)
        except FileNotFoundError:
            cprint('v4l2-ctl not found. Run ./samples/utils/camera/setup.sh script first. Falling back to default index search.', 'yellow')
        except subprocess.CalledProcessError as e:
            cprint(f'Error listing video devices: {e}. Falling back to default index search.')

        if not camera_indices:
            max_tested_cameras = 10
            camera_indices = list(range(max_tested_cameras))

        for index in camera_indices:
            return index
        else:
            raise ValueError('No USB camera found.', 'red')


@dataclass
class RTSPStream:
    host: str
    port: int
    user: str
    password: str
    stream_path: str

    def uri(self) -> str:
        return f'rtsp://{self.user}:{self.password}@{self.host}:{self.port}/{self.stream_path}'


class ONVIFSource:
    def __init__(self, host: str, port: int, user: str, password: str) -> None:
        self._host: str = host
        self._port: int = port
        self._user: str = user
        self._password: str = password
        self._rtsp_stream_list: List[RTSPStream] = []

    def load_onvif(self) -> cv2.VideoCapture:
        my_onvif_source = ONVIFCamera(self._host, self._port, self._user, self._password)
        media = my_onvif_source.create_media_service()
        profiles = media.GetProfiles()
        profile = profiles[0]
        request = media.create_type('GetStreamUri')
        request.ProfileToken = profile.token
        request.StreamSetup = {'Stream': 'RTP-Unicast', 'Transport': {'Protocol': 'RTSP'}}
        response = media.GetStreamUri(request)
        rtsp_stream = RTSPStream(host=self._host, port=self._port, user=self._user, password=self._password, stream_path=response.Uri)
        self._rtsp_stream_list.append(rtsp_stream)

    def print_stream_list(self) -> None:
        for rtsp_stream in self._rtsp_stream_list:
            cprint(rtsp_stream.uri())

    def get_rtsp_stream(self, stream_path: str = '') -> RTSPStream:
        if stream_path:
            for rtsp_stream in self._rtsp_stream_list:
                if rtsp_stream.stream_path == stream_path:
                    return rtsp_stream
        else:
            return self._rtsp_stream_list[0]


class IPCameraSource(CameraSource):
    def __init__(
        self,
        source: Union[RTSPStream, ONVIFSource],
        resolution: tuple[int, int] = (1280, 960),
        fps: int = 60,
    ) -> None:
        '''
        Support below devices

            - C200 Tapo Camera

        '''
        super().__init__(resolution=resolution, fps=fps)

        self._source = source
        self._resoultion = resolution
        self._fps = fps

        self._onvif_source: ONVIFSource = None

    @override
    def cam_on(self) -> None:
        if self._cap is None:
            os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;udp"
            if isinstance(self._source, RTSPStream):
                uri = self._source.uri()
                self._cap = cv2.VideoCapture(uri, cv2.CAP_FFMPEG)
            elif isinstance(self._source, ONVIFSource):
                self._onvif_source = self._source
                self._onvif_source.load_onvif()
                uri = self._source.get_rtsp_stream('stream2').uri()
                self._cap = cv2.VideoCapture(uri, cv2.CAP_FFMPEG)

            if not self._cap.isOpened():
                raise ValueError(f'Cannot open camera at uri {uri}')

            self._cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
            # self._cap.set(cv2.CAP_PROP_FRAME_WIDTH, 99999)
            # self._cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 99999)
        else:
            cprint('Camera is already on.', 'yellow')

        self._cam_on = True

    @override
    def cam_off(self) -> None:
        if self._cap is not None:
            self._cap.release()
            self._cap = None
        else:
            cprint('Camera is already off.', 'yellow')

        self._cam_on = False

    def show_stream(self) -> None:
        while True:
            cv2.imshow('Camera Stream', self.current_frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cv2.destroyAllWindows()


# TODO (thsvkd): Implement PiCamera class
class PiCameraSource(CameraSource):

    def __init__(
        self,
        resolution: tuple[int, int] = (1280, 960),
        fps: int = 60,
    ):
        super().__init__(resolution=resolution, fps=fps)

        self._resolution = resolution
        self._fps = fps
        self.picam2 = Picamera2()
        self.config = self.picam2.create_still_configuration(main={'size': self.resolution})
        self.picam2.configure(self.config)

    @override
    def cam_on(self) -> None:
        self.picam2.start()
        # time.sleep(0.5)  # Wait for camera initialization

        self._cam_on = True

    @override
    def cam_off(self) -> None:
        self.picam2.stop()

        self._cam_on = False

    # def capture_image(self, filename='image.jpg'):
    #     self.picam2.capture_file(filename)
    #     cprint(f'Image captured: {filename}')

    # def start_preview(self):
    #     self.picam2.start_preview()

    # def stop_preview(self):
    #     self.picam2.stop_preview()

    # def record_video(self, filename='video.h264', duration=10, bitrate=10000000):
    #     video_config = self.picam2.create_video_configuration()
    #     self.picam2.configure(video_config)
    #     encoder = H264Encoder(bitrate=bitrate)
    #     self.picam2.start_recording(encoder, filename)
    #     cprint(f'Recording video for {duration} seconds...')
    #     time.sleep(duration)
    #     self.picam2.stop_recording()
    #     cprint(f'Video recorded: {filename}')

    # def change_resolution(self, resolution):
    #     self.resolution = resolution
    #     self.config = self.picam2.create_still_configuration(main={'size': self.resolution})
    #     self.picam2.configure(self.config)

    # def set_controls(self, controls):
    #     self.picam2.set_controls(controls)
