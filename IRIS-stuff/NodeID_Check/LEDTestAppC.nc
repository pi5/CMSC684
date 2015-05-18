configuration LEDTestAppC
{
}
implementation
{
  components MainC, LEDTestC, LedsC;
  components new TimerMilliC() as Timer0;

  LEDTestC -> MainC.Boot;

  LEDTestC.Timer0 -> Timer0;
  LEDTestC.Leds -> LedsC;
}
