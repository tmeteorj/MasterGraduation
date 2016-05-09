package Data;

public class PlaneRecord {
	public int ID;
	public String type;
	public double val[];
	public int size;
	public PlaneRecord(){}
	public PlaneRecord(String []info){
		readInfo(info);
	}
	public void readInfo(String []info){
		//ID,type,attr1,attr2...
		ID=Integer.valueOf(info[0]);
		type=info[1];
		size=info.length-2;
		val=new double[size];
		for(int i=2;i<info.length;i++){
			val[i-2]=Double.valueOf(info[i]);
		}
	}
	
	public String toString(){
		String tp=String.valueOf(ID)+","+type;
		for(int i=0;i<size;i++){
			tp+=","+val[i];
		}
		return tp;
	}
}
