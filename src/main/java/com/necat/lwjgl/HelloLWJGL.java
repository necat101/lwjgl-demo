package com.necat.lwjgl;

import org.lwjgl.Version;
import org.lwjgl.glfw.GLFWErrorCallback;
import org.lwjgl.glfw.GLFWVidMode;
import org.lwjgl.opengl.GL;
import org.lwjgl.system.MemoryStack;

import java.nio.IntBuffer;

import static org.lwjgl.glfw.Callbacks.glfwFreeCallbacks;
import static org.lwjgl.glfw.GLFW.*;
import static org.lwjgl.opengl.GL11.*;
import static org.lwjgl.system.MemoryStack.stackPush;
import static org.lwjgl.system.MemoryUtil.NULL;

/**
 * LWJGL 3 Hello World Demo
 * 
 * Based on the official LWJGL 3 samples and HN discussion:
 * https://news.ycombinator.com/item?id=14797887
 * 
 * This demonstrates the basic LWJGL 3 setup:
 * - GLFW window creation and management
 * - OpenGL context initialization
 * - Basic render loop
 * - Proper resource cleanup
 */
public class HelloLWJGL {

    private long window;

    public void run() {
        System.out.println("Hello LWJGL " + Version.getVersion() + "!");
        System.out.println("LWJGL: Lightweight Java Game Library");
        System.out.println("Based on: https://www.lwjgl.org/");
        System.out.println();

        init();
        loop();

        glfwFreeCallbacks(window);
        glfwDestroyWindow(window);
        glfwTerminate();
        glfwSetErrorCallback(null).free();
        
        System.out.println("Application terminated successfully.");
    }

    private void init() {
        GLFWErrorCallback.createPrint(System.err).set();

        if (!glfwInit()) {
            throw new IllegalStateException("Unable to initialize GLFW");
        }

        glfwDefaultWindowHints();
        glfwWindowHint(GLFW_VISIBLE, GLFW_FALSE);
        glfwWindowHint(GLFW_RESIZABLE, GLFW_TRUE);
        glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
        glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 2);
        glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);
        glfwWindowHint(GLFW_OPENGL_FORWARD_COMPAT, GLFW_TRUE);

        window = glfwCreateWindow(800, 600, "LWJGL Demo - Hello World!", NULL, NULL);
        if (window == NULL) {
            throw new RuntimeException("Failed to create the GLFW window");
        }

        glfwSetKeyCallback(window, (window, key, scancode, action, mods) -> {
            if (key == GLFW_KEY_ESCAPE && action == GLFW_RELEASE) {
                glfwSetWindowShouldClose(window, true);
            }
            if (key == GLFW_KEY_SPACE && action == GLFW_PRESS) {
                System.out.println("Space pressed! LWJGL is working!");
            }
        });

        try (MemoryStack stack = stackPush()) {
            IntBuffer pWidth = stack.mallocInt(1);
            IntBuffer pHeight = stack.mallocInt(1);
            glfwGetWindowSize(window, pWidth, pHeight);
            GLFWVidMode vidmode = glfwGetVideoMode(glfwGetPrimaryMonitor());
            glfwSetWindowPos(
                window,
                (vidmode.width() - pWidth.get(0)) / 2,
                (vidmode.height() - pHeight.get(0)) / 2
            );
        }

        glfwMakeContextCurrent(window);
        glfwSwapInterval(1);
        glfwShowWindow(window);
        
        System.out.println("Window created successfully!");
        System.out.println("Press ESC to exit, SPACE to test input");
        System.out.println();
    }

    private void loop() {
        GL.createCapabilities();

        System.out.println("OpenGL Version: " + glGetString(GL_VERSION));
        System.out.println("OpenGL Vendor: " + glGetString(GL_VENDOR));
        System.out.println("OpenGL Renderer: " + glGetString(GL_RENDERER));
        System.out.println();

        glClearColor(0.1f, 0.15f, 0.3f, 0.0f);

        float hue = 0.0f;
        while (!glfwWindowShouldClose(window)) {
            hue += 0.001f;
            if (hue > 1.0f) hue = 0.0f;
            
            float r = 0.1f + 0.1f * (float)Math.sin(hue * Math.PI * 2);
            float g = 0.15f + 0.1f * (float)Math.sin(hue * Math.PI * 2 + 2);
            float b = 0.3f + 0.1f * (float)Math.sin(hue * Math.PI * 2 + 4);
            
            glClearColor(r, g, b, 1.0f);
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
            glfwSwapBuffers(window);
            glfwPollEvents();
        }
    }

    public static void main(String[] args) {
        System.out.println("=".repeat(60));
        System.out.println("LWJGL 3 Demo Application");
        System.out.println("=".repeat(60));
        System.out.println();
        System.out.println("This demo showcases LWJGL (Lightweight Java Game Library)");
        System.out.println("which provides low-level bindings to native APIs.");
        System.out.println();
        System.out.println("Based on HN Discussion:");
        System.out.println("https://news.ycombinator.com/item?id=14797887");
        System.out.println();
        System.out.println("=".repeat(60));
        System.out.println();
        
        new HelloLWJGL().run();
    }
}
