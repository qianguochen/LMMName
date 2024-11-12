package org.utils;

import java.io.Serializable;
import java.util.List;

/**
 * @description:
 * @author: 大风
 * @date: 2024/9/5 15:33
 */
public class MethodSignatureInfo implements Serializable {

    private List<String> content;

    private Signature signature;

    public List<String> getContent() {
        return content;
    }

    public void setContent(List<String> content) {
        this.content = content;
    }

    public Signature getSignature() {
        return signature;
    }

    public void setSignature(Signature signature) {
        this.signature = signature;
    }

    @Override
    public String toString() {
        final StringBuffer sb = new StringBuffer("MethodSignatureInfo{");
        sb.append("content=").append(content);
        sb.append(", signature=").append(signature);
        sb.append('}');
        return sb.toString();
    }
}
