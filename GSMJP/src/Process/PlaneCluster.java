package Process;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.Properties;

public class PlaneCluster {

	public static void main(String[] args) throws FileNotFoundException, IOException {

		Properties p = new Properties();
		p.load(new FileInputStream(new File("init.properties")));
		String planePath=(String) p.get("planePath");
		System.out.println(planePath);
	}

}
