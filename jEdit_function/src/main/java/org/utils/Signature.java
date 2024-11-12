package org.utils;


import com.github.javaparser.ast.Node;
import com.github.javaparser.ast.body.MethodDeclaration;
import com.github.javaparser.ast.body.Parameter;
import com.github.javaparser.ast.type.Type;

import java.io.Serializable;
import java.util.Arrays;
import java.util.List;
import java.util.Objects;

public class Signature implements Serializable {

	/**
	 * 返回值类型
	 */
	private String return_type;
	/**
	 * 参数类型
	 */
	private String[] paramTypes;
	/**
	 * 参数名称
	 */
	private String[] paramTokens;
	/**
	 * 参数个数
	 */
	private int param_num;

	private String methodName;

	private String methodBody;

	private String currentClass;

	private List<String> importClass;

	private List<String> fields;
	public Signature(MethodDeclaration node) {
		Type returnType = node.getType();
		removeComment(returnType);
		this.return_type = returnType.toString();
		
		List<Parameter> parameters = node.getParameters();
		this.param_num = parameters.size();
		this.paramTypes = new String[this.param_num];
		this.paramTokens = new String[this.param_num];
		
		for(int i = 0; i < parameters.size(); i++) {
			Type paramType = parameters.get(i).getType();
			removeComment(paramType);
			this.paramTypes[i] = paramType.toString();
			this.paramTokens[i] = String.valueOf(parameters.get(i).getName());
		}
		this.methodName = String.valueOf(node.getName());
		if (node.getBody().isPresent()){
			this.methodBody = String.valueOf(node.getBody().get());
		}else {
			this.methodBody = "";
		}
		this.currentClass = node.getClass().getName();
	}
	
	private void removeComment(Node node) {
		node.setComment(null);
		for(Node child : node.getChildNodes()) {
			removeComment(child);
		}
	}

	@Override
	public String toString() {
		String signature = methodName + ';';
			signature += return_type;
		for(int i = 0 ; i < paramTypes.length; i++) {
			signature += ";" + paramTypes[i];
			signature += ";" + paramTokens[i];
		}
		signature += '\n'+methodBody;
		return signature;
	}

//	@Override
//	public int hashCode() {
//		final int prime = 31;
//		int result = 1;
//		int sum = 0;
//		for(String paramType : paramTypes) {
//			int hash = paramType == null ? 0 : paramType.hashCode();
//			sum += hash;
//		}
//		result = prime * result + sum;
//		sum = 0;
//		for(String paramToken : paramTokens) {
//			 int hash = paramToken == null ? 0 : paramToken.hashCode();
//			 sum += hash;
//		}
//		result = prime * result + sum;
//		result = prime * result + ((return_type == null) ? 0 : return_type.hashCode());
//		return result;
//	}
//
//	@Override
//	public boolean equals(Object obj) {
//		if (this == obj)
//			return true;
//		if (obj == null)
//			return false;
//		if (getClass() != obj.getClass())
//			return false;
//		Signature other = (Signature) obj;
//		if (!equals(paramTypes, other.paramTypes))
//			return false;
//		if(!equals(paramTokens, other.paramTokens))
//			return false;
//		if (return_type == null) {
//			if (other.return_type != null)
//				return false;
//		} else if (!return_type.equals(other.return_type))
//			return false;
//		return true;
//	}
//
//	private boolean equals(String[] a, String[] a2) {
//        if (a==a2)
//            return true;
//        if (a==null || a2==null)
//            return false;
//
//        int length = a.length;
//        if (a2.length != length)
//            return false;
//
//        for(int i = 0; i < length; i++) {
//        	int length2 = a2.length;
//        	for(int j = 0; j < length2; j++) {
//        		if(a[i].equals(a2[j])) {
//        			String[] tmp = new String[length2-1];
//        			for(int k = 0; k < j; k++) {
//        				tmp[k] = a2[k];
//        			}
//        			for(int k = j+1; k < length2; k++) {
//        				tmp[k-1] = a2[k];
//        			}
//        			a2 = tmp;
//        			break;
//        		}
//        	}
//        	if(a2.length == length2)
//        		return false;
//        }
//        return true;
//    }


	@Override
	public boolean equals(Object o) {
		if (this == o) return true;
		if (o == null || getClass() != o.getClass()) return false;
		Signature signature = (Signature) o;
		return param_num == signature.param_num && Objects.equals(return_type, signature.return_type) && Arrays.equals(paramTypes, signature.paramTypes) && Arrays.equals(paramTokens, signature.paramTokens) && Objects.equals(methodName, signature.methodName) && Objects.equals(methodBody, signature.methodBody) && Objects.equals(currentClass, signature.currentClass) && Objects.equals(importClass, signature.importClass) && Objects.equals(fields, signature.fields);
	}

	@Override
	public int hashCode() {
		int result = Objects.hash(return_type, param_num, methodName, methodBody, currentClass, importClass, fields);
		result = 31 * result + Arrays.hashCode(paramTypes);
		result = 31 * result + Arrays.hashCode(paramTokens);
		return result;
	}

	public String getReturn_type() {
		return return_type;
	}

	public void setReturn_type(String return_type) {
		this.return_type = return_type;
	}

	public String[] getParamTypes() {
		return paramTypes;
	}

	public void setParamTypes(String[] paramTypes) {
		this.paramTypes = paramTypes;
	}

	public String[] getParamTokens() {
		return paramTokens;
	}

	public void setParamTokens(String[] paramTokens) {
		this.paramTokens = paramTokens;
	}

	public int getParam_num() {
		return param_num;
	}

	public void setParam_num(int param_num) {
		this.param_num = param_num;
	}

	public String getMethodName() {
		return methodName;
	}

	public void setMethodName(String methodName) {
		this.methodName = methodName;
	}

	public String getMethodBody() {
		return methodBody;
	}

	public void setMethodBody(String methodBody) {
		this.methodBody = methodBody;
	}

	public String getCurrentClass() {
		return currentClass;
	}

	public void setCurrentClass(String currentClass) {
		this.currentClass = currentClass;
	}

	public List<String> getImportClass() {
		return importClass;
	}

	public void setImportClass(List<String> importClass) {
		this.importClass = importClass;
	}

	public List<String> getFields() {
		return fields;
	}

	public void setFields(List<String> fields) {
		this.fields = fields;
	}
}
