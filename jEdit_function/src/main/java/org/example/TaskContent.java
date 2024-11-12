package org.example;

import java.nio.file.Files;
import java.nio.file.Path;
import java.util.concurrent.Callable;

/**
 * @description:
 * @author: 大风
 * @date: 2024/7/3 15:52
 */
public class TaskContent implements Callable<Void> {

    String code;
    @Override
    public Void call() {
        FileParserMethodContent fileParserMethodContent =new FileParserMethodContent(code);
        fileParserMethodContent.extractFeatures();
        return null;
    }

    public TaskContent(Path path) {
        try {
            this.code = new String(Files.readAllBytes(path));
        }catch (Exception e){
            e.printStackTrace();
            this.code = "";
        }

    }

    @Override
    public String toString() {
        return "Task{" +
                "code='" + code + '\'' +
                '}';
    }
}
