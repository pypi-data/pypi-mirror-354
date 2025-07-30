__all__ = ['CameraType', 'CameraClient', 'IPCameraSource', 'PiCameraSource']

import os, time, platform
from typing import Union
import cv2

from termcolor import cprint

from .camera_source import USBCameraSource, IPCameraSource, PiCameraSource


class CameraClient:
    # DEFAULT_IMAGE_FOLDER = 'capture_images'
    # DEFAULT_VIDEO_FOLDER = 'video_out'
    # DEFAULT_CONFIG_PATH = 'config.json'

    def __init__(
        self,
        camera_source: Union['USBCameraSource', 'IPCameraSource', 'PiCameraSource'],
        resolution: tuple[int, int] = (1280, 960),
        fps: int = 60,
    ) -> None:
        self._camera_source = camera_source
        self._resoultion = resolution
        self._fps = fps

        if not isinstance(camera_source, (USBCameraSource, IPCameraSource, PiCameraSource)):
            raise ValueError('Invalid camera source type')

    async def init(self):
        await self.camera_source.init()

    async def teardown(self):
        await self.camera_source.teardown()

    def save_current_frame(self, filename: str) -> None:
        while self.camera_source.current_frame is None:
            time.sleep(0.1)
        cv2.imwrite(filename, self.camera_source.current_frame)
        cprint(f'Image saved: {filename}', 'green')

    @property
    def camera_source(self) -> Union['USBCameraSource', 'IPCameraSource', 'PiCameraSource']:
        return self._camera_source

    @property
    def resolution(self) -> tuple[int, int]:
        self._resoultion = self._camera_source.resolution
        return self._resolution

    @property
    def fps(self) -> int:
        self._fps = self._camera_source.fps
        return self._fps

    @property
    def is_cam_on(self) -> bool:
        return self._camera_source.is_cam_on

    @camera_source.setter
    def camera_source(self, camera_source: Union['USBCameraSource', 'IPCameraSource', 'PiCameraSource']) -> None:
        self._camera_source = camera_source

    @resolution.setter
    def resolution(self, resolution: tuple[int, int]) -> None:
        self.camera_source.resolution = resolution
        self._resolution = resolution

    @fps.setter
    def fps(self, fps: int) -> None:
        self.camera_source.fps = fps
        self._fps = fps

    # def make_video(self, src_path=DEFAULT_IMAGE_FOLDER, dst_path=DEFAULT_VIDEO_FOLDER, speed=1.0) -> bool:
    #     try:
    #         cprint(f'Make video start. [video path : {dst_path}]')
    #         self._run_capture = False

    #         image_list = glob(f'{src_path}/*.jpg')
    #         image_list.sort()

    #         fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    #         fps = 30.0 * speed
    #         self._vout = cv2.VideoWriter(dst_path, fourcc, fps, (self._width, self._height))

    #         for image in tqdm(image_list, desc='image read'):
    #             frame = cv2.imread(image)
    #             self._vout.write(frame)
    #         self._vout.release()
    #         cprint(f'Make video finish. [video path : {dst_path}]')

    #         return True
    #     except Exception as e:
    #         cprint(e)
    #         return False

    # def start_capture(self) -> None:
    #     if not self._run_capture:
    #         self._run_capture = True
    #     else:
    #         cprint('thread already run now')

    # def stop_capture(self) -> None:
    #     if self._run_capture:
    #         self._run_capture = False
    #     else:
    #         cprint('thread already stop now')

    # def take_timelapse(self, duration: float, speed: float, folder=DEFAULT_IMAGE_FOLDER, video_path=DEFAULT_VIDEO_FOLDER) -> None:
    #     # Calculate the number of frames to capture based on duration and cycle
    #     total_frames = int(duration * 1000 / self._cycle)
    #     self.start_capture()

    #     cprint(f'Starting timelapse for {duration} seconds, capturing {total_frames} frames.')

    #     # Start the timelapse thread
    #     self.run_thread()

    #     # Wait for the timelapse to complete
    #     time.sleep(duration)
    #     self.stop_capture()

    #     cprint('Timelapse capture completed. Creating video...')

    #     # Create the video from captured images
    #     video_filename = os.path.join(video_path, f'timelapse_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4')
    #     success = self.make_video(src_path=folder, dst_path=video_filename, speed=speed)

    #     if success:
    #         cprint(f'Video created successfully: {video_filename}')
    #     else:
    #         cprint('Failed to create video.')

    # def cap_destroy(self) -> None:
    #     os_bit = platform.architecture()[0]
    #     if self._camera_type in [CameraType.USB, CameraType.IP]:
    #         self._cap.release()
    #     elif self._camera_type == CameraType.PICAMERA and os_bit == '64bit':
    #         self._cap.close()

    # def run(self, user_stop_event: Event, folder=DEFAULT_IMAGE_FOLDER) -> None:
    #     cprint(f'Capture start. [image path : ./{folder}/]')

    #     prev_millis = 0
    #     try:
    #         while not user_stop_event.wait(timeout=0.1):
    #             if (int(round(time.time() * 1000)) - prev_millis) > self._cycle and self._run_capture:
    #                 prev_millis = int(round(time.time() * 1000))
    #                 ret, frame = self._cap.read()
    #                 if ret:
    #                     os.makedirs(folder, exist_ok=True)
    #                     image_name = self.generate_image_name(folder)
    #                     now_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    #                     cv2.imwrite(f'{folder}/{image_name}.jpg', frame)
    #                     cprint(f'[{now_datetime}] Capture success! [press "v" to make video]\r')
    #                     self._capture_num += 1
    #                 else:
    #                     cprint('Camera capture failed!')
    #     except KeyboardInterrupt:
    #         cprint('KeyboardInterrupt... end timelapse')
    #         return False
    #     except Exception as e:
    #         cprint(e)
    #         cprint('while loop end')

    # def run_thread(self) -> None:
    #     self._timelapse_thread.start()

    # def generate_image_name(self, folder: str) -> str:
    #     now = datetime.datetime.now()
    #     capture_date = now.strftime('%Y%m%d')
    #     capture_time = now.strftime('%H%M%S')

    #     image_name = '_'.join([capture_date, capture_time])
    #     image_name_duplicate = glob(f'{folder}/*{image_name}*.jpg')

    #     if len(image_name_duplicate) > 1:
    #         tmp_list = []
    #         for image in image_name_duplicate:
    #             name_split = image.split('_')
    #             if len(name_split) > 2:
    #                 index = image.split('_')[-1][:-4]
    #                 tmp_list.append(int(index))
    #         latest_index = max(tmp_list)

    #         image_name = '_'.join([image_name, str(latest_index + 1)])
    #     elif len(image_name_duplicate) == 1:
    #         image_name += '_1'

    #     return image_name

    # def get_supported_resolutions(self) -> List[str]:
    #     command = f'v4l2-ctl -d {self._cap_num} --list-formats-ext'
    #     result = subprocess.run(command.split(), stdout=subprocess.PIPE, text=True)
    #     output = result.stdout
    #     resolutions = re.findall(r'(\d+)x(\d+)', output)
    #     return list(set(resolutions))

    # def camera_capture(self, image_name: str, cam_num: int = 0) -> bool:
    #     ret = False
    #     try:
    #         if is_raspberry_pi():
    #             if self._camera_type == CameraType.PICAMERA:
    #                 ret = self.save_image_from_picamera(filename=image_name)
    #             else:
    #                 ret = self.save_image_from_usb_camera(filename=image_name)
    #         elif platform.uname().system == 'Darwin':
    #             curr_time = time.time()
    #             while time.time() - curr_time < 0.1:
    #                 ret, frame = self._cap.read()
    #                 cv2.waitKey(30)
    #                 cv2.imwrite(image_name, frame)
    #         elif platform.uname().system == 'Windows':
    #             self._cap.release()
    #             self._cap = cv2.VideoCapture(cam_num, cv2.CAP_DSHOW)
    #             ret, frame = self._cap.read()
    #             cv2.imwrite(image_name, frame)
    #         else:
    #             ret = self.save_image_from_usb_camera(filename=image_name)
    #     except:
    #         return False
    #     finally:
    #         if 'cap' in locals() and not is_raspberry_pi():
    #             cap.release()

    #     return ret

    # def save_image_from_picamera(self, filename: str) -> bool:
    #     try:
    #         camera = Picamera2()
    #         camera_config = camera.create_still_configuration(main={'size': (1920, 1080)})
    #         camera.configure(camera_config)
    #         camera.start()
    #         camera.capture_file(filename)
    #         camera.close()
    #         return True
    #     except Exception as e:
    #         cprint(e)
    #         return False

    # def save_image_from_usb_camera(self, filename: str) -> bool:
    #     try:
    #         self._cap.open(self._cap_num)
    #         self._cap.set(cv2.CAP_PROP_FRAME_WIDTH, 99999)
    #         self._cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 99999)
    #         ret, frame = self._cap.read()
    #         cv2.imwrite(filename, frame)
    #         self._cap.release()
    #         return True
    #     except:
    #         return False

    # def get_cap(self) -> cv2.VideoCapture:
    #     return self._cap
