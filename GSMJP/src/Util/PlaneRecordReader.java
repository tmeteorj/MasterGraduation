package Util;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.List;

import Data.PlaneRecord;

public class PlaneRecordReader {
	public PlaneRecord[] ReadFromFile(String filePath) throws IOException{
		BufferedReader br=new BufferedReader(new InputStreamReader(new FileInputStream(new File(filePath))));
		String line=null;
		List<PlaneRecord> records=new ArrayList<PlaneRecord>();
		while((line=br.readLine())!=null){
			records.add(new PlaneRecord(line.split(",")));
		}
		br.close();
		return records.toArray(new PlaneRecord[records.size()]);
	}
}
