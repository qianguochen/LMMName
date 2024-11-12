package org.example;

import com.github.javaparser.*;
import com.github.javaparser.ast.CompilationUnit;
import org.utils.CountJavaFile;

/**
 * @description:
 * @author: 大风
 * @date: 2024/7/3 16:03
 */
public class FileParserMethodContent {
    private String code;

    private CompilationUnit compilationUnit;
    private JavaParser parser=new JavaParser();

    public FileParserMethodContent(String code) {
        this.code = code;
    }

    public void extractFeatures() {

        try {
            compilationUnit = parseFileWithRetries(code);
        }catch (Exception e){
            e.printStackTrace();
        }

        CountJavaFile.compilationUnits.add(compilationUnit);

    }

    public CompilationUnit parseFileWithRetries(String code) {
        final String classPrefix = "public class Test {";
        final String classSuffix = "}";
        final String methodPrefix = "SomeUnknownReturnType f() {";
        final String methodSuffix = "return noSuchReturnValue; }";
        String originalContent = code;
        String content = originalContent;
        ParseResult<CompilationUnit> parsed = null;
        try {
            parsed = parser.parse(content);
        } catch (ParseProblemException e1) {
            // Wrap with a class and method
            try {
                content = classPrefix + methodPrefix + originalContent + methodSuffix + classSuffix;
                parsed = parser.parse(content);
            } catch (ParseProblemException e2) {
                // Wrap with a class only
                content = classPrefix + originalContent + classSuffix;
                parsed = parser.parse(content);
            }
        }
        return parsed.getResult().get();
    }
}
