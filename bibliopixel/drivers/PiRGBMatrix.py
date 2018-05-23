from . driver_base import DriverBase
from rgbmatrix import RGBMatrix, RGBMatrixOptions


class PiRGBMatrix(DriverBase):
    '''Control a RGB LED matrix using the hzeller/rpi-rgb-led-matrix driver
    Only supported on the Raspberry Pi 2, 3, Zero

    Installing the rpi-rgb-led-matrix driver:

        git clone git@github.com:hzeller/rpi-rgb-led-matrix
        cd rpi-rgb-led-matrix

        make build-python
        sudo -H make install-python
    '''

    def __init__(self, rows=32, cols=32, chain_length=1,
                 parallel=1, pwm_bits=11, brightness=100,
                 hardware_mapping='regular', scan_mode=1,
                 pwm_lsb_nanoseconds=130, show_refresh_rate=False,
                 gpio_slowdown=1, disable_hardware_pulsing=True,
                 led_rgb_sequence='RGB', pixel_mapper_config="",
                 row_address_type=0, multiplexing=0, 
                 debug=False, **kwds):
        '''Initializes a RGB matrix
        Args:
            rows (int): Number of rows in the matrix
            cols (int): Number of columns in the matrix
            chain_length (int): Daisy-chained boards. Default: 1
            parallel (int): Parallel chains. Range 1..3. Default 1
            pwm_bits (int): Bits used for PWM. Range 1..11. Default 11
            brightness (int): Sets brightness level. Range 1..100. Default 100
            hardware_mapping (str): Hardware mapping. Choices: 'regular',
                'adafruit-hat', 'adafruit-hat-pwm'. Default 'regular'
            scan_mode (int): Proressive or interlaced scan.
                0 Progressive, 1 Interlaced (default)
            pwm_lsb_nanoseconds (int): Base time-unit for the on-time in the
                lowest significant bit in nanoseconds. Default: 130
            show_refresh_rate (boolean): Shows the current refresh rate of the LED
                panel. Default: False
            gpio_slowdown (int): Slow down writing to GPIO. Range 1..100.
                Default: 1
            disable_hardware_pulsing (boolean): Don't use hardware pin-pulse generation.
                Default: True
            led_rgb_sequence (str): Color byte order. Default: 'RGB'
            pixel_mapper_config (str): Apply pixel mappers. e.g 'Rotate:90'.
            row_address_type (int): 0=default, 1=AB-addressed panels, 2=row direct
                Default: 0
            multiplexing (int): Multiplexing type. 0=direct, 1=strip, 2=checker,
                3=spiral, 4=ZStripe, 5=ZnMirrorZStripe, 6=coreman, 7=Kaler2Scan,
                8=ZStripeUneven. Default: 0

        '''
        super().__init__(width=cols, height=rows, c_order=led_rgb_sequence, **kwds)

        args = {
            'rows': rows, 'cols': cols, 'chain_length': chain_length,
            'parallel': parallel, 'row_address_type': row_address_type,
            'multiplexing': multiplexing, 'pwm_bits': pwm_bits,
            'brightness': brightness, 'pwm_lsb_nanoseconds': pwm_lsb_nanoseconds,
            'led_rgb_sequence': led_rgb_sequence, 'pixel_mapper_config': pixel_mapper_config,
            'show_refresh_rate': show_refresh_rate, 'gpio_slowdown': gpio_slowdown,
            'disable_hardware_pulsing': disable_hardware_pulsing,
            'hardware_mapping': hardware_mapping
            }

        self.debug = debug

        self.options = RGBMatrixOptions()

        for key, value in args.items():
            setattr(self, key, value)
            setattr(self.options, key, value)
            if debug:
                print("RGBMatrix {}: {}".format(key, value))

        self.matrix = RGBMatrix(options=self.options)
        self.canvas = self.matrix.CreateFrameCanvas()

    def _compute_packet(self):
        self._render()
        data = self._buf
        self._packet = [tuple(data[(p * 3):(p * 3) + 3]) for p in range(len(data) // 3)]

    def _send_packet(self):
        # for y in range(0, self.height):
        #     for x in range(0, self.width):
        for i, p in enumerate(self._packet):
            self.canvas.SetPixel(i % self.cols, i // self.cols, p[0], p[1], p[2])

        self.canvas = self.matrix.SwapOnVSync(self.canvas)

    def set_brightness(self, brightness):
        self.options.brightness = brightness
        self.matrix.brightness = self.options.brightness
        return True
