package Util;

import java.util.Arrays;
import java.util.LinkedList;
import java.util.List;
import java.util.Queue;

import com.sun.jmx.remote.internal.ArrayQueue;

import Data.ClusterResult;
import Data.PlaneRecord;

public class DBSCAN {
	
	public void Cluster(ClusterResult results,PlaneRecord []records,int minPTS,double EPS){
		boolean unSolved[]=new boolean[records.length];
		Arrays.fill(unSolved, true);
		results=new ClusterResult();
		LinkedList<PlaneRecord> list=new LinkedList<PlaneRecord>();
		
	}
}
