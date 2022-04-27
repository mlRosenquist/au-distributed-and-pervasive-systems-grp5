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
    private const string RootTopic = "localhost/";
    private const string LongRangeSensor = "LongRangeSensor";
    private const string ShortRangeSensor = "ShortRangeSensor";
    private const string IkeaMotionSensor = "0x680ae2fffef9a940";
    private const string LightStripActuator = "0x84fd27fffec8a7fd";
    private static List<string> Sensors = new()
    {
        LongRangeSensor,
        ShortRangeSensor,
        IkeaMotionSensor,
        LightStripActuator
    };

    private static bool FridgeClosed = true;
    private static bool PillTaken = false;
    private static DateTime? LastMotionDetected; // not used yet
    private static DateTime? LastPillTaken;
    // Not sure we need to keep state of light. Just send out message to turn it on or off.

    public static async Task Main(string[] args)
    {
        var mqttFactory = new MqttFactory();
        Client = mqttFactory.CreateMqttClient();

        var mqttClientOptions = new MqttClientOptionsBuilder()
            .WithTcpServer("localhost")//.WithTcpServer("86.52.53.126")
            .Build();

        await Client.ConnectAsync(mqttClientOptions, CancellationToken.None);

        foreach (var sensor in Sensors)
        {
            // I guess we don't need to subscribe to lightstrip
            if (sensor == "0x84fd27fffec8a7fd") 
                break;

            var mqttSubscribeOptions = mqttFactory.CreateSubscribeOptionsBuilder()
                       .WithTopicFilter(f => { f.WithTopic($"{RootTopic + sensor}"); })
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
        switch (applicationMessage.Topic)
        {
            case RootTopic + LongRangeSensor:
                FridgeClosed = !FridgeClosed;
                Console.WriteLine($"Fridge Closed: {FridgeClosed}");
                CheckFridgeSafeToEat();
                break;
            case RootTopic + ShortRangeSensor:
                if (!PillTaken)
                {
                    LastPillTaken = DateTime.Now;
                    PillTaken = true;
                }
                Console.WriteLine($"Pill Taken: {PillTaken}");
                break;
            case RootTopic + IkeaMotionSensor:
                LastMotionDetected = DateTime.Now;
                Console.WriteLine($"Motion Detected: {LastMotionDetected}");
                MotionSensorSequence();
                break;
            default:
                throw new ArgumentException("Unknown Topic");
        }

        // Message debugging
        Console.WriteLine("inside listen event");
        Console.WriteLine(applicationMessage.Topic);
        var payload = System.Text.Encoding.UTF8.GetString(applicationMessage.Payload);
        var data = JsonConvert.DeserializeObject<ProximitySensorEvent>(payload);
        Console.WriteLine(data.DeviceId);
        Console.WriteLine(data.DeviceDescription);
        Console.WriteLine(data.Payload);



        return Task.CompletedTask;
    }

    internal static void CheckFridgeSafeToEat()
    {
        if (!PillTaken && !FridgeClosed)
        {
            // send warning light
            TurnOnLightStrip();
        } else
        {
            TurnOffLightStrip();
        }

    }

    public static void TurnOnLightStrip()
    {
        var applicationMessage = new MqttApplicationMessageBuilder()
            .WithTopic($"{RootTopic + LightStripActuator}/set")
            .WithPayload("{" +
                         "\"state\": \"ON\", \n" +
                         $"\"brightness\": \"200\", \n" +
                         $"\"color\": {{\"hex\": \"#EE401A\"}} \n" +
                         "}")
            .Build();

        Client.PublishAsync(applicationMessage, CancellationToken.None);

        Console.WriteLine("Fridge Warning Light ON");
    }


    public static void TurnOffLightStrip()
    {
        var applicationMessage = new MqttApplicationMessageBuilder()
            .WithTopic($"{RootTopic + LightStripActuator}/set")
            .WithPayload("{\"state\": \"OFF\"}")
            .Build();

        Client.PublishAsync(applicationMessage, CancellationToken.None);


        Console.WriteLine("Fridge Warning Light OFF");
    }

    internal static void MotionSensorSequence()
    {
        Console.WriteLine("Commencing wake up sequence");
        // Maybe waking up. Check if last taken pill was not today. Maybe patient need to sleep, so we track that with
        // motion sensor, before patient should take medicine again.
        if (LastPillTaken.Value.Date != DateTime.Today)
        {
            PillTaken = false;
        }
    }

    internal class ProximitySensorEvent
    {
        public string? DeviceId { get; set; }
        public string? DeviceDescription { get; set; }
        public string? Payload { get; set; }
    }
}