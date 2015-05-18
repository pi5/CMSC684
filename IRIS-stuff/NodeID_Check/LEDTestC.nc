#include "Timer.h"

module LEDTestC @safe()
{
  uses interface Timer<TMilli> as Timer0;
  uses interface Leds;
  uses interface Boot;
}
implementation
{
  event void Boot.booted()
  {
    call Timer0.startPeriodic( 250 );
  }

  event void Timer0.fired()
  {
    if (TOS_NODE_ID == 0) {
      call Leds.led0Toggle();
    } else if (TOS_NODE_ID == 1) {
      call Leds.led1Toggle();
    } else if (TOS_NODE_ID == 2) {
      call Leds.led2Toggle();
    }
  }
}
