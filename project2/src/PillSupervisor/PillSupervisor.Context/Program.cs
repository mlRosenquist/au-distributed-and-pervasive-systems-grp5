using MQTTnet;
using MQTTnet.Client;
using Newtonsoft.Json;
using System;
using PillSupervisor.Business;
// Context model proposal from Alexander
// It's a state machine *MIND BLOWN* emoji
public static class Program
{
    // ZigBee messages are sent with MQTT messages as specified in Business
    // Phidget messages are with MQTT messages as specified in SensorHandling
    // State will have to be set based on message from sensors: LongRange, ShortRange, IkeaMotion

    // Motion Sensor is used to check if it's a new day (as the patient is waking up), and resets so the pill needs
    // to be taken again.

    // The context model shouldn't initialize the sensors, as it is in the backend, and only communicates with the sensors through MQTT messages.
    // Phidget init will have to be done on the pc/microcontroller that they are connected to it. Same for the ZigBee units, as they
    // are connected to the dongle-hub, then the mc for the dongle hub, will have to take care of MQTT comms. to context.


    // What about when will pill taken be reset?

    private static MqttClient? Client { get; set; }
    private const string LongRangeTopic = "Proximitysensor/LongRangeSensor";
    private const string ShortRangeTopic = "Proximitysensor/ShortRangeSensor";
    private const string IkeaMotionSensor = "zigbee2mqtt/0x680ae2fffef9a940";
    private const string WarningLightActuator = "zigbee2mqtt/0x84fd27fffec8a7fd";
    private static List<string> Sensors = new()
    {
        LongRangeTopic,
        ShortRangeTopic,
        IkeaMotionSensor,
        WarningLightActuator
    };
    private const string ContextTopic = "Context";

    private static bool FridgeOpen = true;
    private static bool PillTaken = false;
    private static DateTime? LastMotionDetected; // not used yet
    private static DateTime? LastPillTaken = DateTime.Now - TimeSpan.FromDays(1);
    // Not sure we need to keep state of light. Just send out message to turn it on or off.

    public static async Task Main(string[] args)
    {
        var mqttFactory = new MqttFactory();
        Client = mqttFactory.CreateMqttClient();

        var mqttClientOptions = new MqttClientOptionsBuilder()
            //.WithTcpServer("localhost")
            .WithTcpServer("86.52.53.126")
            .Build();

        await Client.ConnectAsync(mqttClientOptions, CancellationToken.None);

        foreach (var sensor in Sensors)
        {
            // I guess we don't need to subscribe to lightstrip
            if (sensor == "0x84fd27fffec8a7fd")
                break;

            var mqttSubscribeOptions = mqttFactory.CreateSubscribeOptionsBuilder()
                       .WithTopicFilter(f => { f.WithTopic($"{sensor}"); })
                       .Build();

            await Client.SubscribeAsync(mqttSubscribeOptions, CancellationToken.None);
        }



        // listen on sensor event
        Console.WriteLine("before listen event");
        Client.ApplicationMessageReceivedAsync += e => ContextUpdate(e.ApplicationMessage);

        Console.ReadLine();
    }

    public static Task ContextUpdate(MqttApplicationMessage applicationMessage)
    {

        var payloadString = System.Text.Encoding.UTF8.GetString(applicationMessage.Payload);
        switch (applicationMessage.Topic)
        {
            case LongRangeTopic:
                var proximitySensorEvent = JsonConvert.DeserializeObject<ProximitySensorEvent>(payloadString);
                if (proximitySensorEvent != null && proximitySensorEvent.Status != null)
                {
                    FridgeOpen = proximitySensorEvent.Status.Contains("Open");
                }

                CheckFridgeSafeToEat();
                break;
            case ShortRangeTopic:
                if (!PillTaken)
                {
                    LastPillTaken = DateTime.Now;
                    PillTaken = true;
                }
                break;
            case IkeaMotionSensor:
                var ikeaMotionEvent = JsonConvert.DeserializeObject<IkeaMotionEvent>(payloadString);
                if (ikeaMotionEvent.occupancy.Value)
                {
                    LastMotionDetected = DateTime.Now;
                    MotionSensorSequence();
                }
                break;
            case WarningLightActuator:
                Console.WriteLine("Reply from lightstrip?");
                break;
            default:
                throw new ArgumentException("Unknown Topic");
        }
        Console.WriteLine($"Fridge Open: {FridgeOpen}");
        Console.WriteLine($"Pill Taken: {PillTaken}");
        Console.WriteLine($"Motion Detected: {LastMotionDetected}");
        Console.WriteLine($"Last Pill Taken: {LastPillTaken}");
        Console.WriteLine($"Time since pill taken: {(DateTime.Now - LastPillTaken).Value.Seconds}");
        Console.WriteLine("\n");

        return Task.CompletedTask;
    }

    internal static void CheckFridgeSafeToEat()
    {
        if ((FridgeOpen && !PillTaken) || (FridgeOpen && PillTakenWithinHour()))
        {
            // send warning light
            SendMedicineWarningStatus(true);
        }
        else
        {
            SendMedicineWarningStatus(false);
        }

    }

    private static bool PillTakenWithinHour()
    {
        return (DateTime.Now - LastPillTaken.Value) <= TimeSpan.FromSeconds(30);//.FromHours(1);
    }

    public async static void SendMedicineWarningStatus(bool sendWarning)
    {
        //var warningState = sendWarning ? "ON" : "OFF";

        var lightStripSetPayload = new LightStripSetEvent()
        {
            state = $"ON",
            brightness = "200",
            color = new LightStripSetColor()
            {
                hex = "#EE401A",
            },
        };

        if (!sendWarning)
        {
            lightStripSetPayload.color.hex = "#1AEE2E";
        }

        var payloadJson = JsonConvert.SerializeObject(lightStripSetPayload);

        await Client.PublishStringAsync($"{WarningLightActuator}/set", payload: payloadJson);

        Console.WriteLine($"Fridge Warning Light {sendWarning}");
    }

    internal static void MotionSensorSequence()
    {
        Console.WriteLine("Commencing wake up sequence");
        // Maybe waking up. Check if last taken pill was not today. Maybe patient need to sleep, so we track that with
        // motion sensor, before patient should take medicine again.

        //if (LastPillTaken.Value.Date != DateTime.Today)

        if ((DateTime.Now - LastPillTaken.Value) >= TimeSpan.FromSeconds(90)) ; // Demonstration value
        {
            PillTaken = false;
        }
    }

    internal class LightStripSetColor
    {
        public string? hex { get; set; }
    }

    internal class LightStripSetEvent
    {
        public string? state { get; set; }
        public string? brightness { get; set; }
        public LightStripSetColor? color { get; set; }
    }


    internal class ProximitySensorEvent
    {
        public string? DeviceId { get; set; }
        public string? DeviceDescription { get; set; }
        public string? Status { get; set; }
    }

    internal class IkeaMotionEvent
    {
        public bool? occupancy { get; set; }
    }
}