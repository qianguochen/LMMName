package org.utils;

import java.util.List;

/**
 * @description:
 * @author: 大风
 * @date: 2024/7/4 8:53
 */
public class JavaFileInfo {

    private String className;

    private List<Signature> signatures;

    public JavaFileInfo() {
    }

    public JavaFileInfo(String className, List<Signature> signatures) {
        this.className = className;
        this.signatures = signatures;
    }

    public String getClassName() {
        return className;
    }

    public void setClassName(String className) {
        this.className = className;
    }

    public List<Signature> getSignatures() {
        return signatures;
    }

    public void setSignatures(List<Signature> signatures) {
        this.signatures = signatures;
    }

}
