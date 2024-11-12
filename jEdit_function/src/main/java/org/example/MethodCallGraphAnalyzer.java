package org.example;

import com.github.javaparser.ast.CompilationUnit;
import com.github.javaparser.ast.body.ClassOrInterfaceDeclaration;
import com.github.javaparser.ast.body.MethodDeclaration;
import com.github.javaparser.ast.expr.Expression;
import com.github.javaparser.ast.expr.MethodCallExpr;
import com.github.javaparser.ast.visitor.VoidVisitorAdapter;
import org.utils.*;

import java.io.IOException;
import java.util.*;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.CopyOnWriteArrayList;

public class MethodCallGraphAnalyzer {

    private static List<Signature> signatures = new CopyOnWriteArrayList<>();

    private static Map<Signature, MethodSignatureInfo> infoMap = new ConcurrentHashMap<>();

    public static void doAnalyzer(String path) throws IOException {

        List<CompilationUnit> compilationUnits = CountJavaFile.compilationUnits;

        for (CompilationUnit compilationUnit : compilationUnits) {
            new MethodDeclarationVisitor().visit(compilationUnit, null);
        }
        for (CompilationUnit compilationUnit : compilationUnits) {
            new MethodCallVisitor().visit(compilationUnit, null);
        }
        List<MethodSignatureInfo> list = new ArrayList<>();

        for (Map.Entry<Signature, MethodSignatureInfo> entry : infoMap.entrySet()) {
            list.add(entry.getValue());
        }
        System.out.println(signatures.size());
        System.out.println(list.size());
        System.out.println("接口：" + CountJavaFile.countInterface.get());
        System.out.println("类：" + CountJavaFile.countClass.get());
        System.out.println("行数：" + CountJavaFile.countLines.get());
        System.out.println("方法数量：" + CountJavaFile.countMethod.get());
        System.out.println("失败次数：" + CountJavaFile.countFail.get());
        System.out.println("Java文件：" + CountJavaFile.compilationUnits.size());
        System.out.println(Executor.javaFile.size());
        FileUtils.writeMethodSignatureContent(list, path);
    }

    static class MethodCallVisitor extends VoidVisitorAdapter<Void> {
        @Override
        public void visit(ClassOrInterfaceDeclaration n, Void arg) {
            if (!n.isInterface()) {
                for (MethodDeclaration methodDeclaration : n.getMethods()) {
                    if (methodDeclaration.getBody().isPresent()) {
                        methodDeclaration.accept(new VoidVisitorAdapter<Void>() {
                            @Override
                            public void visit(MethodCallExpr n, Void arg) {
                                for (Signature signature : signatures) {
                                    String methodName = signature.getMethodName();
                                    int paramsSize = signature.getParam_num();
                                    List<String> arguments = new ArrayList<>();
                                    for (Expression expression : n.getArguments()) {
                                        String argument = expression.toString();
                                        arguments.add(argument);
                                    }
                                    if (Objects.equals(methodName, n.getNameAsString()) && paramsSize == arguments.size()) {
                                        if (!infoMap.containsKey(signature)) {
                                            List<String> signatureListContent = new ArrayList<>();
                                            MethodSignatureInfo methodSignatureInfo = new MethodSignatureInfo();
                                            signatureListContent.add(String.valueOf(methodDeclaration));
                                            methodSignatureInfo.setContent(signatureListContent);
                                            methodSignatureInfo.setSignature(signature);
                                            infoMap.put(signature, methodSignatureInfo);
                                        } else {
                                            MethodSignatureInfo methodSignatureInfo = infoMap.get(signature);
                                            List<String> signatureList = methodSignatureInfo.getContent();
                                            signatureList.add(String.valueOf(methodDeclaration));
                                            infoMap.put(signature, methodSignatureInfo);
                                        }
                                    }
                                }
                                super.visit(n, arg);
                            }
                        }, null);
                    }
                }
            }
            super.visit(n, arg);
        }
    }

    static class MethodDeclarationVisitor extends VoidVisitorAdapter<Void> {
        @Override
        public void visit(ClassOrInterfaceDeclaration n, Void arg) {
            if (!n.isInterface()) {
                CountJavaFile.countClass.getAndAdd(1);
                for (MethodDeclaration methodDeclaration : n.getMethods()) {
                    if (methodDeclaration.getBody().isPresent()) {
                        Signature signature = new Signature(methodDeclaration);
                        signature.setCurrentClass(String.valueOf(n.getName()));
                        CountJavaFile.countMethod.incrementAndGet();
                        signatures.add(signature);
                        int lines = methodDeclaration.getEnd().get().line - methodDeclaration.getBegin().get().line + 1;
                        CountJavaFile.countLines.getAndAdd(lines);
                    }
                }
            } else {
                CountJavaFile.countInterface.incrementAndGet();
            }
            super.visit(n, arg);
        }
    }
}