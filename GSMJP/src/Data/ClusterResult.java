package Data;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.util.ArrayList;
import java.util.List;

public class ClusterResult {
	public List<List<PlaneRecord>> result;
	public void init(){
		result.clear();
	}
	public void addOneCluster(List<PlaneRecord> itemlist){
		result.add(itemlist);
	}
	public void writeToFile(String filePath) throws IOException{
		OutputStreamWriter osw=new OutputStreamWriter(new FileOutputStream(new File(filePath)));
		int INDEX=0;
		for(List<PlaneRecord> itemlist:result){
			for(PlaneRecord item:itemlist){
				osw.write(INDEX+","+item.toString()+"\n");
			}
			INDEX++;
		}
		osw.close();
	}
}
