package org.utils;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.io.FileWriter;
import java.util.List;



/**
 * @description:
 * @author: 大风
 * @date: 2024/7/4 9:55
 */
public class FileUtils {

    public static void javaFileWrite(List<Signature> signatures,String path) throws JsonProcessingException {
        ObjectMapper objectMapper = new ObjectMapper();
        for (Signature signature : signatures) {
            String content = objectMapper.writeValueAsString(signature);
            try (FileWriter fileWriter = new FileWriter(path, true)) {
                synchronized (FileUtils.class){
                    fileWriter.write(content + '\n');
                }
            } catch (Exception e) {
                e.printStackTrace();
                CountJavaFile.countFail.incrementAndGet();
            }
        }
    }

    public static void writeMethodSignatureContent(List<MethodSignatureInfo> methodSignatureInfos,String path) throws JsonProcessingException {
        ObjectMapper objectMapper = new ObjectMapper();
        for (MethodSignatureInfo methodSignatureInfo : methodSignatureInfos){
            String content = objectMapper.writeValueAsString(methodSignatureInfo);
            try(FileWriter fileWriter = new FileWriter(path, true)){
                synchronized (FileUtils.class){
                    fileWriter.write(content+'\n');
                }
            }catch (Exception e){
                e.printStackTrace();
            }
        }
    }
}
