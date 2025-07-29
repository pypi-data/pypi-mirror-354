import board
import adafruit_bh1750
from termcolor import cprint


class LightSensor:
    """
    단일 BH1750 광도 센서 관리 클래스

    단일 BH1750 광도 센서를 관리하는 클래스입니다. I2C 직접 연결 또는
    멀티플렉서 채널을 통한 연결을 모두 지원하며, Adafruit 스타일의
    간편한 API를 제공합니다.

    Features:
        - BH1750 광도 센서 제어
        - I2C 직접 연결 및 멀티플렉서 지원
        - 자동 오류 처리 및 fallback 값 제공
        - Adafruit 스타일 프로퍼티 접근
        - 상세한 오류 로깅

    Hardware Requirements:
        - Raspberry Pi with I2C enabled
        - BH1750 light sensor
        - Proper I2C connections (SDA, SCL, VCC, GND)
        - Pull-up resistors (usually built-in on Pi)

    I2C Address:
        - Default: 0x23 (35 decimal)
        - Alternative: 0x5C (92 decimal) with ADDR pin high

    Supported I2C Objects:
        - board.I2C() (Direct I2C connection)
        - Multiplexer channels (mux[0], mux[1], etc.)
        - Any object with I2C interface

    Example:
        Direct I2C connection:
        >>> import board
        >>> from device.light_sensor import LightSensor
        >>>
        >>> sensor = LightSensor(board.I2C())
        >>> print(f"Lux: {sensor.lux}")
        >>> print(f"Status: {sensor.status}")

        With Multiplexer:
        >>> import adafruit_tca9548a
        >>> mux = adafruit_tca9548a.PCA9546A(board.I2C())
        >>> sensor = LightSensor(mux[0])

        Error handling:
        >>> sensor = LightSensor(board.I2C())
        >>> if sensor.is_connected:
        >>>     print(f"Light level: {sensor.lux} lux")
        >>> else:
        >>>     print("Sensor not available")

    Attributes:
        _i2c: I2C 통신 객체
        _sensor (BH1750 | None): BH1750 센서 객체, 실패 시 None
        _is_connected (bool): 센서 연결 상태

    Raises:
        ValueError: I2C 주소에 장치가 없는 경우
        OSError: I2C 통신 오류 (Errno 121 등)
        ImportError: 필요한 라이브러리가 설치되지 않은 경우

    Notes:
        - 센서 초기화 실패 시 lux 프로퍼티는 -1을 반환합니다
        - 런타임 중 센서 오류 발생 시 자동으로 오류 메시지가 출력됩니다
        - I2C 멀티플렉서 사용 시 채널 전환은 자동으로 처리됩니다
    """

    def __init__(self, i2c, address: int = 0x23):
        """
        LightSensor 초기화

        I2C 인터페이스를 통해 BH1750 센서를 초기화합니다.
        센서 연결에 실패해도 객체 생성은 성공하며, 상태는 is_connected로 확인할 수 있습니다.

        Args:
            i2c: I2C 통신 객체
                - board.I2C(): 직접 I2C 연결
                - mux[n]: 멀티플렉서 채널
                - I2C 인터페이스를 가진 모든 객체
            address (int, optional): I2C 주소. Defaults to 0x23.
                                   일반적으로 기본값 사용, ADDR 핀 연결 시 0x5C

        Raises:
            ImportError: adafruit_bh1750 라이브러리가 설치되지 않은 경우
                        해결: pip install adafruit-circuitpython-bh1750

        Example:
            >>> # 직접 연결
            >>> sensor = LightSensor(board.I2C())

            >>> # 멀티플렉서 연결
            >>> mux = adafruit_tca9548a.PCA9546A(board.I2C())
            >>> sensor = LightSensor(mux[0])

            >>> # 사용자 정의 주소
            >>> sensor = LightSensor(board.I2C(), address=0x5C)
        """
        self._i2c = i2c
        self._address = address
        self._sensor = None
        self._is_connected = False

        # BH1750 센서 초기화 시도
        try:
            self._sensor = adafruit_bh1750.BH1750(self._i2c, address=self._address)
            self._is_connected = True
            cprint(f"✓ BH1750 센서 초기화 성공 (주소: 0x{self._address:02X})", "green")
        except (ValueError, OSError) as e:
            self._sensor = None
            self._is_connected = False
            cprint(f"✗ BH1750 센서 초기화 실패 - {e}", "red")

    @property
    def is_connected(self) -> bool:
        """
        센서 연결 상태 확인

        센서가 정상적으로 초기화되고 연결되어 있는지 확인합니다.

        Returns:
            bool: 센서 연결 상태
                 - True: 센서가 정상 연결됨
                 - False: 센서 연결 실패 또는 오류

        Example:
            >>> sensor = LightSensor(board.I2C())
            >>> if sensor.is_connected:
            >>>     print("센서 사용 가능")
            >>> else:
            >>>     print("센서 연결 확인 필요")
        """
        return self._is_connected

    @property
    def lux(self) -> float:
        """
        조도 측정값 (lux)

        센서에서 현재 조도 값을 읽어와서 반환합니다.
        센서가 연결되지 않았거나 읽기에 실패한 경우 -1을 반환합니다.

        Returns:
            float: 조도 값 (lux)
                  - 정상값: 0.0 ~ 65535.0 lux
                  - 오류값: -1.0 (센서 오류 또는 연결 실패)

        Raises:
            None: 모든 예외는 내부에서 처리되며 -1을 반환

        Example:
            >>> sensor = LightSensor(board.I2C())
            >>> lux_value = sensor.lux
            >>> if lux_value >= 0:
            >>>     print(f"조도: {lux_value:.2f} lux")
            >>> else:
            >>>     print("센서 읽기 실패")
        """
        if not self._is_connected or self._sensor is None:
            return -1.0

        try:
            return float(self._sensor.lux)
        except (ValueError, OSError, RuntimeError) as e:
            cprint(f"BH1750 센서 읽기 오류: {e}", "red")
            return -1.0

    @property
    def lux_string(self) -> str:
        """
        조도 측정값을 문자열로 반환

        조도 값을 소수점 4자리까지 포맷된 문자열로 반환합니다.
        오류 시에는 "-1" 문자열을 반환합니다.

        Returns:
            str: 포맷된 조도 값 문자열
                - 정상: "245.8333" (소수점 4자리)
                - 오류: "-1"

        Example:
            >>> sensor = LightSensor(board.I2C())
            >>> lux_str = sensor.lux_string
            >>> print(f"조도: {lux_str} lux")
        """
        lux_value = self.lux
        if lux_value >= 0:
            return f"{lux_value:.4f}"
        else:
            return "-1"

    @property
    def status(self) -> str:
        """
        센서 상태 문자열

        센서의 현재 상태를 사람이 읽기 쉬운 문자열로 반환합니다.

        Returns:
            str: 센서 상태
                - "working": 센서가 정상 작동 중
                - "failed": 센서 초기화 실패 또는 연결되지 않음

        Example:
            >>> sensor = LightSensor(board.I2C())
            >>> print(f"센서 상태: {sensor.status}")
        """
        return "working" if self._is_connected else "failed"

    def read_lux(self) -> float:
        """
        조도 값 읽기 (메소드 방식)

        lux 프로퍼티와 동일한 기능을 메소드로 제공합니다.
        일부 코딩 스타일에서 명시적 메소드 호출을 선호할 때 사용합니다.

        Returns:
            float: 조도 값 (lux) 또는 -1 (오류 시)

        Example:
            >>> sensor = LightSensor(board.I2C())
            >>> lux_value = sensor.read_lux()
            >>> print(f"측정된 조도: {lux_value} lux")
        """
        return self.lux

    def reset_connection(self) -> bool:
        """
        센서 연결 재시도

        센서 연결이 실패했거나 문제가 있을 때 재연결을 시도합니다.
        런타임 중 센서가 분리되었다가 다시 연결된 경우에 유용합니다.

        Returns:
            bool: 재연결 성공 여부
                 - True: 재연결 성공
                 - False: 재연결 실패

        Example:
            >>> sensor = LightSensor(board.I2C())
            >>> if not sensor.is_connected:
            >>>     if sensor.reset_connection():
            >>>         print("센서 재연결 성공")
            >>>     else:
            >>>         print("센서 재연결 실패")
        """
        try:
            self._sensor = adafruit_bh1750.BH1750(self._i2c, address=self._address)
            self._is_connected = True
            cprint(f"✓ BH1750 센서 재연결 성공 (주소: 0x{self._address:02X})", "green")
            return True
        except (ValueError, OSError) as e:
            self._sensor = None
            self._is_connected = False
            cprint(f"✗ BH1750 센서 재연결 실패 - {e}", "red")
            return False

    def get_sensor_info(self) -> dict:
        """
        센서 정보 반환

        센서의 상태, 주소, 연결 정보를 딕셔너리로 반환합니다.
        디버깅이나 시스템 상태 점검에 유용합니다.

        Returns:
            dict: 센서 정보
                - address: I2C 주소 (16진수 문자열)
                - is_connected: 연결 상태 (bool)
                - status: 상태 문자열
                - sensor_type: 센서 타입

        Example:
            >>> sensor = LightSensor(board.I2C())
            >>> info = sensor.get_sensor_info()
            >>> print(f"센서 정보: {info}")
            {'address': '0x23', 'is_connected': True, 'status': 'working', 'sensor_type': 'BH1750'}
        """
        return {'address': f'0x{self._address:02X}', 'is_connected': self._is_connected, 'status': self.status, 'sensor_type': 'BH1750'}


def test_light_sensor() -> None:
    """
    LightSensor 클래스의 기본 기능을 테스트하는 함수

    직접 I2C 연결을 통해 센서를 초기화하고 모든 기능을 테스트합니다.
    센서 연결, 데이터 읽기, 상태 확인 등의 기능을 검증합니다.

    Test Coverage:
        - 센서 초기화 (board.I2C 사용)
        - 연결 상태 확인 (is_connected)
        - 조도 값 읽기 (lux, lux_string, read_lux)
        - 센서 정보 조회 (get_sensor_info)
        - 재연결 테스트 (reset_connection)

    Expected Output:
        - 센서 초기화 성공/실패 메시지
        - 조도 측정값 (정상 시) 또는 오류 메시지 (실패 시)
        - 센서 상태 및 정보 출력

    Error Handling:
        - ImportError: CircuitPython 라이브러리 미설치
        - OSError: I2C 통신 오류, 센서 연결 문제
        - ValueError: 잘못된 I2C 주소 또는 설정
    """
    cprint("LightSensor 테스트 시작...")

    try:
        # I2C 버스 초기화
        i2c = board.I2C()

        # 센서 초기화
        sensor = LightSensor(i2c)

        # 센서 정보 출력
        cprint(f"센서 정보: {sensor.get_sensor_info()}")

        if sensor.is_connected:
            cprint("✓ 센서가 정상적으로 연결되었습니다", "green")

            # 조도 값 읽기 (여러 방법)
            lux_value = sensor.lux
            lux_string = sensor.lux_string
            lux_method = sensor.read_lux()

            cprint(f"조도 (프로퍼티): {lux_value:.4f} lux")
            cprint(f"조도 (문자열): {lux_string} lux")
            cprint(f"조도 (메소드): {lux_method:.4f} lux")
            cprint(f"센서 상태: {sensor.status}")

            # 광도 범위에 따른 해석
            if lux_value > 1000:
                cprint("📍 밝은 환경 (직사광선 또는 강한 조명)")
            elif lux_value > 100:
                cprint("📍 일반 실내 조명 환경")
            elif lux_value > 10:
                cprint("📍 어두운 실내 환경")
            else:
                cprint("📍 매우 어두운 환경")

        else:
            cprint("✗ 센서 연결 실패 - 하드웨어 연결을 확인하세요", "red")

            # 재연결 시도
            cprint("재연결 시도 중...", "yellow")
            if sensor.reset_connection():
                cprint("재연결 성공!", "green")
                cprint(f"조도: {sensor.lux:.4f} lux")
            else:
                cprint("재연결 실패")

    except ImportError as e:
        cprint(f"라이브러리 오류: {e}", "red")
        cprint("필요한 라이브러리 설치:", "yellow")
        cprint("  pip install adafruit-circuitpython-bh1750", "yellow")
        cprint("  pip install adafruit-circuitpython-busdevice", "yellow")
    except Exception as e:
        cprint(f"예상치 못한 오류: {e}", "red")


def test_with_multiplexer() -> None:
    """
    I2C 멀티플렉서와 함께 LightSensor를 사용하는 예제

    PCA9546A 멀티플렉서의 여러 채널에서 센서를 테스트합니다.
    멀티플렉서를 사용하면 동일한 I2C 주소를 가진 여러 센서를
    하나의 버스에서 사용할 수 있습니다.

    Hardware Setup:
        - Raspberry Pi I2C 버스
        - PCA9546A 또는 TCA9548A 멀티플렉서
        - BH1750 센서들 (각 채널에 연결)

    Test Coverage:
        - 멀티플렉서 초기화
        - 여러 채널의 센서 테스트
        - 채널별 독립적 동작 확인

    Dependencies:
        - adafruit-circuitpython-busdevice
        - adafruit-circuitpython-bh1750
        - adafruit-circuitpython-tca9548a
    """
    try:
        import adafruit_tca9548a

        print("멀티플렉서를 사용한 LightSensor 테스트...")

        # I2C 버스 및 멀티플렉서 초기화
        i2c = board.I2C()
        mux = adafruit_tca9548a.PCA9546A(i2c)

        # 여러 채널에서 센서 테스트
        sensors = []
        for ch in range(4):  # PCA9546A는 4채널
            print(f"\n--- 채널 {ch} 테스트 ---")
            sensor = LightSensor(mux[ch])
            sensors.append(sensor)

            if sensor.is_connected:
                print(f"채널 {ch} 조도: {sensor.lux:.4f} lux")
            else:
                print(f"채널 {ch} 센서 없음")

        # 연결된 센서들 요약
        working_sensors = [i for i, s in enumerate(sensors) if s.is_connected]
        print(f"\n정상 작동 센서: 채널 {working_sensors}")
        print(f"총 {len(working_sensors)}/4개 센서 작동 중")

    except ImportError as e:
        print(f"라이브러리 오류: {e}")
        print("필요한 라이브러리 설치:")
        print("  pip install adafruit-circuitpython-bh1750")
        print("  pip install adafruit-circuitpython-tca9548a")
    except Exception as e:
        print(f"예상치 못한 오류: {e}")


if __name__ == "__main__":
    # 기본 센서 테스트
    test_light_sensor()

    print("\n" + "=" * 50 + "\n")

    # 멀티플렉서 테스트
    test_with_multiplexer()
