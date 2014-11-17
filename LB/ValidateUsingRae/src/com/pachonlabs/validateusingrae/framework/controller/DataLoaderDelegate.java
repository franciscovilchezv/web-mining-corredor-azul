package com.pachonlabs.validateusingrae.framework.controller;

public interface DataLoaderDelegate {
	public void didStartLoadingData();
	public void didFinishLoadingData(Object data);
}
