__version__ = '1.0.0'
__author__ = 'alisonsalmeida'


from machine import Pin, SPI


class MCP3008:
    SINGLE = 1
    DIFFERENTIAL = 0

    def __init__(self, channel, spi: SPI, cs: Pin, v_ref=3300):
        """
        Inicializa o MCP3008
        :param spi: Interface SPI para ler e escrever os dados
        :param cs: Pino CS para selecionar o device
        :param v_ref: tensao de referencia em mili volts
        """

        if channel > 7:
            raise RuntimeError('channel must be less or equal 7')

        self.channel = channel
        self.spi = spi
        self.cs = cs
        self.v_ref = v_ref
        self.cs(1)

        self._value = 0
        self._resolution = 10

    async def read(self, input_type=SINGLE):
        """
        Retorna um numero inteiro de 0 a 1023 0u None caso nao consiga lê o conversor AD
        :param channel: canal a ser lido.
        :param input_type: tipo de leitura, single ou diferencial
        :return:

        0 - tipo de leitura single ou diferencial
        0 - canal a ser lido
        0 - canal a ser lido
        0 - canal a ser lido

        X - não importa
        X - não importa
        X - não importa
        X - não importa

        http://ww1.microchip.com/downloads/en/DeviceDoc/21295d.pdf#G1.1035395
        """

        try:
            self.cs(0)                         # Seleciona o conversor AD
            self.spi.write(b'\x01')            # envia um start bit

            # configura o tipo de leitura
            config = ((input_type << 3) + self.channel) << 4

            hdata = self.spi.read(1, config)   # seleciona o tipo de leitura e o canal enquanto le um byte.
            ldata = self.spi.read(1)           # le o byte menos significativo

            ldata = int.from_bytes(ldata, 'little')
            hdata = int.from_bytes(hdata, 'little')

        except Exception as e:
            return None

        finally:
            self.cs(1)                        # libera o conversor AD

        self._value = (hdata << 8) + ldata
        return self._value

    @property
    def voltage(self):
        return None

    @voltage.getter
    def voltage(self) -> float:
        return (self._value * (self.v_ref / 1000)) / (1 << self._resolution)

    def __str__(self):
        return f'<MCP3008 - Channel: {self.channel}>'
