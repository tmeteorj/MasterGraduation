package Util;

import Data.PlaneRecord;

public class PlaneCalc {
	public double distance(PlaneRecord a,PlaneRecord b){
		if(a.size!=b.size){
			System.err.println("Size is not equal for records: "+a+" / "+b);
			System.exit(-1);
		}
		double top=a.type.equals(b.type)?1:0,bota=1,botb=1;
		for(int i=0;i<a.size;i++){
			top+=a.val[i]*b.val[i];
			bota+=a.val[i]*a.val[i];
			botb+=b.val[i]*b.val[i];
		}
		return top/Math.sqrt(bota*botb);
	}
}
