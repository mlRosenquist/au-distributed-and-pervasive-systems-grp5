using System;
using System.Timers;
using Phidget22;

namespace Phidget.SensorHandling
{
	class Program
	{
		private static void VoltageInput_VoltageChangeLongRange(object sender, Phidget22.Events.VoltageInputVoltageChangeEventArgs e)
		{
			Phidget22.VoltageInput evChannel = (Phidget22.VoltageInput)sender;
			// Long range goes fast from 5 to 0
			var active = e.Voltage < 1;
			if (active)
				Console.WriteLine($"Long range is active!");


		}

		private static void VoltageInput_VoltageChangeCloseRange(object sender, Phidget22.Events.VoltageInputVoltageChangeEventArgs e)
		{
			Phidget22.VoltageInput evChannel = (Phidget22.VoltageInput)sender;
			// Close range goes unstable from 5 to 0.5, so bigger step for stability
			var active = e.Voltage < 2;
			if (active)
				Console.WriteLine($"Close is active!");
		}

		static void Main(string[] args)
		{
			VoltageInput voltageInputLongRange = new VoltageInput();
			VoltageInput voltageInputCloseRange = new VoltageInput();

			voltageInputLongRange.DeviceSerialNumber = 265779;
			voltageInputLongRange.Channel = 0;
			voltageInputCloseRange.DeviceSerialNumber = 265779;
			voltageInputCloseRange.Channel = 1;

			voltageInputLongRange.VoltageChange += VoltageInput_VoltageChangeLongRange;
			voltageInputCloseRange.VoltageChange += VoltageInput_VoltageChangeCloseRange;

			voltageInputLongRange.Open(5000);
			voltageInputLongRange.VoltageChangeTrigger = 1;
			voltageInputCloseRange.Open(5000);
			voltageInputCloseRange.VoltageChangeTrigger = 3;

			//Wait until Enter has been pressed before exiting
			Console.ReadLine();

			voltageInputLongRange.Close();
			voltageInputCloseRange.Close();
		}
	}
}