package com.necat.lwjgl;

import org.lwjgl.Version;
import org.lwjgl.glfw.GLFWErrorCallback;
import org.lwjgl.glfw.GLFWVidMode;
import org.lwjgl.opengl.GL;
import org.lwjgl.system.MemoryStack;

import java.nio.IntBuffer;
import java.util.HashMap;
import java.util.Map;

import static org.lwjgl.glfw.Callbacks.glfwFreeCallbacks;
import static org.lwjgl.glfw.GLFW.*;
import static org.lwjgl.opengl.GL11.*;
import static org.lwjgl.system.MemoryStack.stackPush;
import static org.lwjgl.system.MemoryUtil.NULL;

/**
 * LWJGL 3 Hello World Demo with Command-Line Configuration
 * 
 * Supports dynamic configuration via command-line flags for rapid testing
 * without Maven rebuilds. Use with Python launcher for best experience.
 * 
 * @see https://github.com/necat101/lwjgl-demo
 */
public class HelloLWJGL {

    private static class Config {
        int width = 800;
        int height = 600;
        String title = "LWJGL Demo - Hello World!";
        boolean vsync = true;
        boolean fullscreen = false;
        boolean resizable = true;
        float clearR = 0.1f;
        float clearG = 0.15f;
        float clearB = 0.3f;
        boolean animate = true;
        float animateSpeed = 1.0f;
        boolean printGlInfo = false;
    }

    private final Config config = new Config();
    private long window;

    public HelloLWJGL(String[] args) {
        parseArgs(args);
    }

    private void parseArgs(String[] args) {
        Map<String, String> argMap = new HashMap<>();
        
        for (int i = 0; i < args.length; i++) {
            String arg = args[i];
            if (arg.equals("--help") || arg.equals("-h")) {
                printHelp();
                System.exit(0);
            } else if (arg.startsWith("--")) {
                String key = arg.substring(2);
                String value = "true";
                if (i + 1 < args.length && !args[i + 1].startsWith("--")) {
                    value = args[++i];
                }
                argMap.put(key, value);
            }
        }

        if (argMap.containsKey("width")) config.width = Integer.parseInt(argMap.get("width"));
        if (argMap.containsKey("height")) config.height = Integer.parseInt(argMap.get("height"));
        if (argMap.containsKey("title")) config.title = argMap.get("title");
        if (argMap.containsKey("vsync")) config.vsync = argMap.get("vsync").equals("1") || argMap.get("vsync").equalsIgnoreCase("true");
        if (argMap.containsKey("fullscreen")) config.fullscreen = true;
        if (argMap.containsKey("not-resizable")) config.resizable = false;
        if (argMap.containsKey("clear-r")) config.clearR = Float.parseFloat(argMap.get("clear-r"));
        if (argMap.containsKey("clear-g")) config.clearG = Float.parseFloat(argMap.get("clear-g"));
        if (argMap.containsKey("clear-b")) config.clearB = Float.parseFloat(argMap.get("clear-b"));
        if (argMap.containsKey("animate")) config.animate = !argMap.get("animate").equals("0") && !argMap.get("animate").equalsIgnoreCase("false");
        if (argMap.containsKey("animate-speed")) config.animateSpeed = Float.parseFloat(argMap.get("animate-speed"));
        if (argMap.containsKey("print-gl-info")) config.printGlInfo = true;
    }

    private void printHelp() {
        System.out.println("LWJGL Demo - Command Line Options");
        System.out.println("==================================");
        System.out.println();
        System.out.println("Window: --width, --height, --title, --fullscreen, --not-resizable");
        System.out.println("Graphics: --vsync <0|1>, --clear-r/g/b <0.0-1.0>");
        System.out.println("Animation: --animate <0|1>, --animate-speed <float>");
        System.out.println("Other: --print-gl-info, --help");
        System.out.println();
        System.out.println("Examples:");
        System.out.println("  --width 1024 --height 768");
        System.out.println("  --fullscreen --vsync 0");
        System.out.println("  --clear-r 0.5 --clear-g 0 --clear-b 0.5 --animate-speed 2.0");
    }

    public void run() {
        System.out.println("Hello LWJGL " + Version.getVersion() + "!");
        System.out.println("Config: " + config.width + "x" + config.height + 
                          (config.fullscreen ? " fullscreen" : "") +
                          " vsync=" + (config.vsync ? "on" : "off"));
        System.out.println();

        init();
        
        if (config.printGlInfo) {
            printGLInfo();
            cleanup();
            return;
        }
        
        loop();
        cleanup();
    }

    private void init() {
        GLFWErrorCallback.createPrint(System.err).set();
        if (!glfwInit()) throw new IllegalStateException("Unable to initialize GLFW");

        glfwDefaultWindowHints();
        glfwWindowHint(GLFW_VISIBLE, GLFW_FALSE);
        glfwWindowHint(GLFW_RESIZABLE, config.resizable ? GLFW_TRUE : GLFW_FALSE);
        glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
        glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 2);
        glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);
        glfwWindowHint(GLFW_OPENGL_FORWARD_COMPAT, GLFW_TRUE);

        long monitor = config.fullscreen ? glfwGetPrimaryMonitor() : NULL;
        window = glfwCreateWindow(config.width, config.height, config.title, monitor, NULL);
        if (window == NULL) throw new RuntimeException("Failed to create window");

        glfwSetKeyCallback(window, (window, key, scancode, action, mods) -> {
            if (key == GLFW_KEY_ESCAPE && action == GLFW_RELEASE) {
                glfwSetWindowShouldClose(window, true);
            }
            if (key == GLFW_KEY_SPACE && action == GLFW_PRESS) {
                System.out.println("Space pressed!");
            }
        });

        if (!config.fullscreen) {
            try (MemoryStack stack = stackPush()) {
                IntBuffer pWidth = stack.mallocInt(1);
                IntBuffer pHeight = stack.mallocInt(1);
                glfwGetWindowSize(window, pWidth, pHeight);
                GLFWVidMode vidmode = glfwGetVideoMode(glfwGetPrimaryMonitor());
                glfwSetWindowPos(window, (vidmode.width() - pWidth.get(0)) / 2,
                                       (vidmode.height() - pHeight.get(0)) / 2);
            }
        }

        glfwMakeContextCurrent(window);
        glfwSwapInterval(config.vsync ? 1 : 0);
        glfwShowWindow(window);
        System.out.println("Window created. Press ESC to exit, SPACE to test input.\n");
    }

    private void printGLInfo() {
        GL.createCapabilities();
        System.out.println("=== OpenGL Information ===");
        System.out.println("Version:  " + glGetString(GL_VERSION));
        System.out.println("Vendor:   " + glGetString(GL_VENDOR));
        System.out.println("Renderer: " + glGetString(GL_RENDERER));
        System.out.println("==========================");
    }

    private void loop() {
        GL.createCapabilities();
        System.out.println("OpenGL: " + glGetString(GL_VERSION) + "\n");

        glClearColor(config.clearR, config.clearG, config.clearB, 1.0f);

        float hue = 0.0f;
        while (!glfwWindowShouldClose(window)) {
            if (config.animate) {
                hue += 0.001f * config.animateSpeed;
                if (hue > 1.0f) hue = 0.0f;
                float r = config.clearR + 0.1f * (float)Math.sin(hue * Math.PI * 2);
                float g = config.clearG + 0.1f * (float)Math.sin(hue * Math.PI * 2 + 2);
                float b = config.clearB + 0.1f * (float)Math.sin(hue * Math.PI * 2 + 4);
                glClearColor(Math.max(0, Math.min(1, r)), Math.max(0, Math.min(1, g)), 
                           Math.max(0, Math.min(1, b)), 1.0f);
            }
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
            glfwSwapBuffers(window);
            glfwPollEvents();
        }
    }

    private void cleanup() {
        glfwFreeCallbacks(window);
        glfwDestroyWindow(window);
        glfwTerminate();
        glfwSetErrorCallback(null).free();
        System.out.println("Application terminated successfully.");
    }

    public static void main(String[] args) {
        System.out.println("=".repeat(60));
        System.out.println("LWJGL 3 Demo with Dynamic Configuration");
        System.out.println("=".repeat(60));
        System.out.println();
        
        if (args.length > 0 && (args[0].equals("--help") || args[0].equals("-h"))) {
            new HelloLWJGL(new String[0]).printHelp();
            return;
        }
        
        try {
            new HelloLWJGL(args).run();
        } catch (Exception e) {
            System.err.println("Error: " + e.getMessage());
            e.printStackTrace();
            System.exit(1);
        }
    }
}
