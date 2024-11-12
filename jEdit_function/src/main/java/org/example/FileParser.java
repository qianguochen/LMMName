package org.example;

import com.github.javaparser.JavaParser;
import com.github.javaparser.ParseProblemException;
import com.github.javaparser.ParseResult;
import com.github.javaparser.ast.CompilationUnit;
import com.github.javaparser.ast.body.ClassOrInterfaceDeclaration;
import com.github.javaparser.ast.body.MethodDeclaration;
import com.github.javaparser.ast.visitor.VoidVisitorAdapter;
import org.utils.CountJavaFile;
import org.utils.Signature;

import java.io.IOException;
import java.util.ArrayList;

import java.util.List;


/**
 * @description:
 * @author: 大风
 * @date: 2024/7/3 16:03
 */
public class FileParser {
    private String code;
    private CompilationUnit compilationUnit;

    private JavaParser parser=new JavaParser();

    public FileParser(String code) {
        this.code = code;
    }

    public void extractFeatures() throws IOException {
        try {
            compilationUnit = parseFileWithRetries(code);
        }catch (Exception e){
            e.printStackTrace();
        }
        CountJavaFile.compilationUnits.add(compilationUnit);
        new MethodCallVisitor().visit(compilationUnit,null);
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

    static class MethodCallVisitor extends VoidVisitorAdapter<Void> {
        @Override
        public void visit(ClassOrInterfaceDeclaration n, Void arg) {
            if (!n.isInterface()) {
                List<Signature> signatures = new ArrayList<>();
                CountJavaFile.countClass.getAndAdd(1);
                for (MethodDeclaration methodDeclaration : n.getMethods()) {
                    if (methodDeclaration.getBody().isPresent()) {
                        Signature signature = new Signature(methodDeclaration);
                        signature.setCurrentClass(String.valueOf(n.getName()));
                        signatures.add(signature);
                        CountJavaFile.countMethod.incrementAndGet();
                        CountJavaFile.signatures.add(signature);
                        int lines = methodDeclaration.getEnd().get().line - methodDeclaration.getBegin().get().line + 1;
                        CountJavaFile.countLines.getAndAdd(lines);
                    }
                }
                if (signatures.size() == 0) {
                    System.out.println("该类没有方法");
                    CountJavaFile.countFail.incrementAndGet();
                }
            }else {
                CountJavaFile.countInterface.incrementAndGet();
            }
            super.visit(n, arg);
        }
    }
}
