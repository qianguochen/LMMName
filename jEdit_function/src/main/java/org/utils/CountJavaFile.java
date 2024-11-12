package org.utils;

import com.github.javaparser.ast.CompilationUnit;
import java.util.List;
import java.util.concurrent.CopyOnWriteArrayList;
import java.util.concurrent.atomic.AtomicInteger;

/**
 * @description:
 * @author: 大风
 * @date: 2024/7/4 9:58
 */
public class CountJavaFile {

    public static AtomicInteger countClass =new AtomicInteger();
    public static AtomicInteger countInterface =new AtomicInteger();
    public static AtomicInteger countMethod = new AtomicInteger();

    public static AtomicInteger countLines =new AtomicInteger();

    public static AtomicInteger countFail = new AtomicInteger();

    public static List<CompilationUnit> compilationUnits = new CopyOnWriteArrayList<>();

    public static List<Signature> signatures = new CopyOnWriteArrayList<>();
}
