using System;
using System.Timers;
using Phidget22;
using MQTTnet;
using MQTTnet.Client;
using Newtonsoft.Json;

namespace Phidget.SensorHandling
{
	public class Program
	{
        private static MqttClient? Client { get; set; }
		
        private async static void VoltageInput_VoltageChangeLongRange(object sender, Phidget22.Events.VoltageInputVoltageChangeEventArgs e)
		{
			Phidget22.VoltageInput evChannel = (Phidget22.VoltageInput)sender;
			// Long range goes fast from 5 to 0
			var active = e.Voltage < 1;
			if (!active)
				return;

			Console.WriteLine($"Long range is active!");

			var payload = new ProximitySensorEvent()
			{
				DeviceId = "101",
				DeviceDescription = "Long range device",
				Payload = "Fired!",
				Date = DateTime.UtcNow
			};

			var payloadJson = JsonConvert.SerializeObject(payload);

			await Client.PublishStringAsync("LongRangeSensor", payload: payloadJson);
		}

		private async static void VoltageInput_VoltageChangeCloseRange(object sender, Phidget22.Events.VoltageInputVoltageChangeEventArgs e)
		{
			Phidget22.VoltageInput evChannel = (Phidget22.VoltageInput)sender;
			// Close range goes unstable from 5 to 0.5, so bigger step for stability
			var active = e.Voltage < 2;
			if (!active)
				return;

			Console.WriteLine($"Close is active!");

			var payload = new ProximitySensorEvent()
			{
				DeviceId = "102",
				DeviceDescription = "Short range device",
				Payload = "Fired!",
				Date = DateTime.UtcNow
			};

			var payloadJson = JsonConvert.SerializeObject(payload);

			await Client.PublishStringAsync("ShortRangeSensor", payload: payloadJson);
		}

		static async Task Main(string[] args)
		{
			// Init MQQT Client
			var mqttFactory = new MqttFactory();
			Client = mqttFactory.CreateMqttClient();

			var mqttClientOptions = new MqttClientOptionsBuilder()
				.WithTcpServer("86.52.53.126")
				.Build();

			await Client.ConnectAsync(mqttClientOptions, CancellationToken.None);

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

    public class ProximitySensorEvent
	{
        public string? DeviceId { get; set; }
        public string? DeviceDescription { get; set; }
        public string? Payload { get; set; }
        public DateTime? Date { get; set; }
    }
}