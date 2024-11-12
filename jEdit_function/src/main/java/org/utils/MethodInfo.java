package org.utils;

import java.util.List;

/**
 * @description:
 * @author: 大风
 * @date: 2024/9/3 15:33
 */
public class MethodInfo {

    private String methodName;
    private List<String> methodParams;
    private String methodParentNode;

    public String getMethodName() {
        return methodName;
    }

    public void setMethodName(String methodName) {
        this.methodName = methodName;
    }

    public List<String> getMethodParams() {
        return methodParams;
    }

    public void setMethodParams(List<String> methodParams) {
        this.methodParams = methodParams;
    }

    public String getMethodParentNode() {
        return methodParentNode;
    }

    public void setMethodParentNode(String methodParentNode) {
        this.methodParentNode = methodParentNode;
    }

    @Override
    public String toString() {
        final StringBuffer sb = new StringBuffer("MethodInfo{");
        sb.append("methodName='").append(methodName).append('\'');
        sb.append(", methodParams=").append(methodParams);
        sb.append(", methodParentNode='").append(methodParentNode).append('\'');
        sb.append('}');
        return sb.toString();
    }
}
