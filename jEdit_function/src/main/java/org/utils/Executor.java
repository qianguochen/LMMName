package org.utils;

import org.example.Task;
import org.example.TaskContent;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.LinkedList;
import java.util.List;
import java.util.concurrent.CopyOnWriteArrayList;
import java.util.concurrent.Executors;
import java.util.concurrent.ThreadPoolExecutor;

/**
 * @description:
 * @author: 大风
 * @date: 2024/7/3 15:42
 */
public class Executor {

    public static List<String> javaFile =new CopyOnWriteArrayList<>();
    public static void executeDir(int numThreads,String dir){
        ThreadPoolExecutor executor = (ThreadPoolExecutor) Executors.newFixedThreadPool(numThreads);
        LinkedList<Task> tasks =new LinkedList<Task>();

        try {
            Files.walk(Paths.get(dir)).filter(Files::isRegularFile)
                    .filter(p->p.toString().toLowerCase().endsWith(".java")).forEach(f ->{
                        Task task=new Task(f);
                        tasks.add(task);
                    });
        }catch (IOException e){
            e.printStackTrace();
            return;
        }
        try {
            executor.invokeAll(tasks);
        }catch (InterruptedException e){
            e.printStackTrace();
        }finally {
            executor.shutdown();
        }
    }
    public static void executeDirContent(int numThreads,String dir){
        ThreadPoolExecutor executor = (ThreadPoolExecutor) Executors.newFixedThreadPool(numThreads);
        LinkedList<TaskContent> tasks =new LinkedList<TaskContent>();
        try {
            Files.walk(Paths.get(dir)).filter(Files::isRegularFile)
                    .filter(p->p.toString().toLowerCase().endsWith(".java")).forEach(f ->{
                        TaskContent task= new TaskContent(f);
                        javaFile.add(f.toString());
                        tasks.add(task);
                    });
        }catch (IOException e){
            e.printStackTrace();
            return;
        }
        try {
            executor.invokeAll(tasks);
        }catch (InterruptedException e){
            e.printStackTrace();
        }finally {
            executor.shutdown();
        }
    }
}
