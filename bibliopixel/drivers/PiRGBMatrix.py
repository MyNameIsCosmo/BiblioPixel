from . driver_base import DriverBase
from rgbmatrix import RGBMatrix, RGBMatrixOptions


class PiRGBMatrix(DriverBase):
    '''Control a RGB LED matrix using the hzeller/rpi-rgb-led-matrix driver
    Only supported on the Raspberry Pi 2, 3, Zero

    Installing the rpi-rgb-led-matrix driver:

        git clone git@github.com:hzeller/rpi-rgb-led-matrix
        cd rpi-rgb-led-matrix

        make build-python
        make install-python
    '''

    def __init__(self, rows=32, cols=32, chain=1,
                 parallel=1, pwm_bits=11, brightness=100,
                 gpio_mapping='regular', scan_mode=1,
                 pwm_lsb_nanoseconds=130, show_refresh=False,
                 slowdown_gpio=1, no_hardware_pulse=True,
                 rgb_sequence='RGB', pixel_mapper="",
                 row_addr_type=0, multiplexing=0, **kwds):
        '''Initializes a RGB matrix
        Args:
            rows (int): Number of rows in the matrix
            cols (int): Number of columns in the matrix
            chain (int): Daisy-chained boards. Default: 1
            parallel (int): Parallel chains. Range 1..3. Default 1
            pwm_bits (int): Bits used for PWM. Range 1..11. Default 11
            brightness (int): Sets brightness level. Range 1..100. Default 100
            gpio_mapping (str): Hardware mapping. Choices: 'regular',
                'adafruit-hat', 'adafruit-hat-pwm'. Default 'regular'
            scan_mode (int): Proressive or interlaced scan.
                0 Progressive, 1 Interlaced (default)
            pwm_lsb_nanoseconds (int): Base time-unit for the on-time in the
                lowest significant bit in nanoseconds. Default: 130
            show_refresh (boolean): Shows the current refresh rate of the LED
                panel. Default: False
            slowdown_gpio (int): Slow down writing to GPIO. Range 1..100.
                Default: 1
            no_hardware_pulse (boolean): Don't use hardware pin-pulse generation.
                Default: True
            rgb_sequence (str): Color byte order. Default: 'RGB'
            pixel_mapper (str): Apply pixel mappers. e.g 'Rotate:90'.
            row_addr_type (int): 0=default, 1=AB-addressed panels, 2=row direct
                Default: 0
            multiplexing (int): Multiplexing type. 0=direct, 1=strip, 2=checker,
                3=spiral, 4=ZStripe, 5=ZnMirrorZStripe, 6=coreman, 7=Kaler2Scan,
                8=ZStripeUneven. Default: 0

        '''
        super().__init__(width=cols, height=rows, c_order=rgb_sequence, **kwds)

        options = RGBMatrixOptions()
        options.hardware_mapping = gpio_mapping
        options.rows = rows
        options.cols = cols
        options.chain_length = chain
        options.parallel = parallel
        options.row_address_type = row_addr_type
        options.multiplexing = multiplexing
        options.pwm_bits = pwm_bits
        options.brightness = brightness
        options.pwm_lsb_nanoseconds = pwm_lsb_nanoseconds
        options.led_rgb_sequence = rgb_sequence
        options.pixel_mapper_config = pixel_mapper
        options.show_refresh_rate = show_refresh
        options.gpio_slowdown = slowdown_gpio
        options.disable_hardware_pulsing = no_hardware_pulse

        self.matrix = RGBMatrix(options=options)
        self.canvas = self.matrix.CreateFrameCanvas()

    def _compute_packet(self):
        self._render()
        data = self._buf
        self._packet = [tuple(data[(p * 3):(p * 3) + 3]) for p in range(len(data) // 3)]

    def _send_packet(self):
        # for y in range(0, self.height):
        #     for x in range(0, self.width):
        for i, p in enumerate(self._packet):
            self.canvas.SetPixel(i // self.cols, i % self.cols, p[0], p[1], p[2])

        self.matrix.SwapOnVSync(self.canvas)

    def set_brightness(self, brightness):
        self.matrix.brightness = brightness
        return True
