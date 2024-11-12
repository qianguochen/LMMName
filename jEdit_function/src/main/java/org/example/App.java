package org.example;

import com.fasterxml.jackson.core.JsonProcessingException;
import org.common.CommandLineValues;
import org.kohsuke.args4j.CmdLineException;
import org.utils.CountJavaFile;
import org.utils.Executor;
import org.utils.FileUtils;

import java.io.IOException;

/**
 * Hello world!
 */
public class App {
    private static CommandLineValues commandLineValues;
    public static void main(String[] args) throws JsonProcessingException {
        try {
            commandLineValues = new CommandLineValues(args);
            System.out.println(commandLineValues);
            String savePath = commandLineValues.fileName+".csv";
            if (!commandLineValues.isContainContent){
                Executor.executeDir(commandLineValues.NumThreads, commandLineValues.Dir);
                FileUtils.javaFileWrite(CountJavaFile.signatures,savePath);
            }else {
                Executor.executeDirContent(commandLineValues.NumThreads, commandLineValues.Dir);
                MethodCallGraphAnalyzer.doAnalyzer(savePath);
            }
        } catch (CmdLineException | IOException e) {
            throw new RuntimeException(e);
        }
        System.out.println("接口" + CountJavaFile.countInterface.get());
        System.out.println("类" + CountJavaFile.countClass.get());
        System.out.println("行数" + CountJavaFile.countLines.get());
        System.out.println("方法数量" + CountJavaFile.countMethod.get());
        System.out.println("失败次数" + CountJavaFile.countFail.get());
        System.out.println("Java文件" + CountJavaFile.compilationUnits.size());
    }
}
