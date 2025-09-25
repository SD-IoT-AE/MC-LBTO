package stam;

import java.util.*;
import java.util.concurrent.*;

/**
 * STAMController.java
 * -------------------
 * Java-based implementation of the Secure Trusted Adaptive Multi-Control (STAM) module,
 * coordinating SDN controllers with secure communication, PDSM integration, and adaptive logic.
 */
public class STAMController {

    // ========== PHASE 1: Initialization ==========
    private static final String controllerId = "ctrlA";
    private static final String controllerKey = "alpha_secret";
    private static final Set<String> authenticatedControllers = new HashSet<>();
    private static final Map<String, String> sharedKeys = Map.of(
        "ctrlA", "alpha_secret",
        "ctrlB", "beta_secret"
    );

    // ========== Controller State & TCC ==========
    private static final Map<String, String> controllerState = new ConcurrentHashMap<>();
    private static final Map<String, String> TCC = new ConcurrentHashMap<>();

    // Simulated PDSM metric input
    static class PDSMReport {
        double trafficVolume;
        double delay;
        boolean congestionAlert;

        PDSMReport(double tv, double d, boolean c) {
            trafficVolume = tv;
            delay = d;
            congestionAlert = c;
        }
    }

    public static void main(String[] args) {
        initialize();
        createSecureChannel();

        System.out.println("🔐 STAM Controller Initialized and Secure Channels Established.\n");

        // Start continuous operation and monitoring loop
        Timer timer = new Timer();
        timer.scheduleAtFixedRate(new TimerTask() {
            public void run() {
                continuousOperationLoop();
            }
        }, 0, 6000); // Run every 6 seconds
    }

    // ========== PHASE 1: Initialization ==========
    private static void initialize() {
        for (String controller : sharedKeys.keySet()) {
            if (authenticate(controller, sharedKeys.get(controller))) {
                authenticatedControllers.add(controller);
                System.out.println("✅ Authenticated: " + controller);
            } else {
                System.out.println("❌ Authentication Failed: " + controller);
            }
        }
    }

    private static boolean authenticate(String id, String key) {
        return sharedKeys.containsKey(id) && sharedKeys.get(id).equals(key);
    }

    // ========== PHASE 2: Secure Channel Setup ==========
    private static void createSecureChannel() {
        for (String ci : authenticatedControllers) {
            for (String cj : authenticatedControllers) {
                if (!ci.equals(cj)) {
                    String tccKey = generateTCCKey(ci, cj);
                    TCC.put(ci + "-" + cj, tccKey);
                }
            }
        }
    }

    private static String generateTCCKey(String c1, String c2) {
        return Integer.toHexString(Objects.hash(c1, c2));
    }

    // ========== PHASE 3-7: Continuous Monitoring and Adaptation ==========
    private static void continuousOperationLoop() {
        System.out.println("\n🔄 Continuous Monitoring Triggered...");

        // PHASE 3: Receive & Process PDSM Metrics
        PDSMReport report = receivePDSMReport();
        processPDSM(report);

        // PHASE 4: Evaluate Controller State
        boolean overloaded = isControllerOverloaded(report);
        boolean adaptationNeeded = overloaded || report.congestionAlert;

        // PHASE 5-6: Trigger Adaptation
        if (adaptationNeeded) {
            adaptControlInterfaces(report);
        }

        // PHASE 7: Feedback Loop
        monitorAndRefine(report);
    }

    private static PDSMReport receivePDSMReport() {
        Random r = new Random();
        return new PDSMReport(
            0.5 + r.nextDouble() * 0.8, // traffic volume
            0.1 + r.nextDouble() * 0.3, // delay
            r.nextDouble() > 0.75       // congestion alert
        );
    }

    private static void processPDSM(PDSMReport report) {
        System.out.printf("📡 PDSM Data: Traffic=%.2f, Delay=%.2f, Alert=%b%n",
                report.trafficVolume, report.delay, report.congestionAlert);
    }

    private static boolean isControllerOverloaded(PDSMReport report) {
        return report.trafficVolume > 1.0 || report.delay > 0.3;
    }

    private static void adaptControlInterfaces(PDSMReport report) {
        System.out.println("⚙️  Adaptation Triggered...");
        for (String ci : authenticatedControllers) {
            System.out.printf("🔧 Adjusting control parameters for %s...%n", ci);
            System.out.printf("🔄 Syncing PALB policies (e.g., server weights) for %s...%n", ci);
            broadcastTCC(ci, report);
        }
    }

    private static void broadcastTCC(String fromController, PDSMReport report) {
        for (String peer : authenticatedControllers) {
            if (!peer.equals(fromController)) {
                String tccId = fromController + "-" + peer;
                System.out.printf("📨 [%s] → [%s] via TCC [%s]: Update PALB weights, prioritize queue alerts%n",
                        fromController, peer, TCC.get(tccId).substring(0, 8));
            }
        }
    }

    private static void monitorAndRefine(PDSMReport report) {
        System.out.println("🔁 Feedback Phase: Monitoring adaptation impact...");
        double improvement = 0.05 + new Random().nextDouble() * 0.1;
        System.out.printf("📈 Performance improved by %.2f%% post-adaptation.%n", improvement * 100);
    }
}
