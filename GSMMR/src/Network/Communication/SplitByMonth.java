package Network.Communication;

import java.io.IOException;
import java.util.Iterator;

import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapred.FileInputFormat;
import org.apache.hadoop.mapred.FileOutputFormat;
import org.apache.hadoop.mapred.JobClient;
import org.apache.hadoop.mapred.JobConf;
import org.apache.hadoop.mapred.MapReduceBase;
import org.apache.hadoop.mapred.Mapper;
import org.apache.hadoop.mapred.OutputCollector;
import org.apache.hadoop.mapred.Reducer;
import org.apache.hadoop.mapred.Reporter;
import org.apache.hadoop.mapred.TextInputFormat;
import org.apache.hadoop.mapred.TextOutputFormat;

public class SplitByMonth {
	public static class SplitMapper extends MapReduceBase
			implements
				Mapper<LongWritable, Text, Text, Text> {
		private Text m_key = new Text();
		private Text m_value = new Text();

		public void map(LongWritable key, Text value,
				OutputCollector<Text, Text> output, Reporter reporter)
				throws IOException {
			String line = value.toString();
			String[] info = line.split(",");
			// type,time,small-big,id1,id2
			String month = info[1].substring(0, 6);
			String flag = null;
			if (info[3].compareTo(info[4]) <= 0) {
				m_key.set(month + "," + info[3] + "," + info[4]);
				flag = ",0";
			} else {
				m_key.set(month + "," + info[4] + "," + info[3]);
				flag = ",1";
			}
			int type = Integer.parseInt(info[0]);
			switch (type) {
				case 1 :
					m_value.set("1,0,0,0" + flag);
					break;
				case 3 :
					m_value.set("0,1,0,0" + flag);
					break;
				case 6 :
					m_value.set("0,0,1,0" + flag);
					break;
				case 7 :
					m_value.set("0,0,0,1" + flag);
					break;
			}
			output.collect(m_key, m_value);
		}
	}

	public static class SplitCombiner extends MapReduceBase
			implements
				Reducer<Text, Text, Text, Text> {
		public void reduce(Text key, Iterator<Text> values,
				OutputCollector<Text, Text> output, Reporter reporter)
				throws IOException {

			int cnt[][] = new int[2][4];
			for (int i = 0; i < 2; i++) {
				for (int j = 0; j < 4; j++) {
					cnt[i][j] = 0;
				}
			}
			while (values.hasNext()) {
				String info[] = values.next().toString().split(",");
				int id = Integer.parseInt(info[4]);
				for (int i = 0; i < 4; i++) {
					cnt[id][i] += Integer.parseInt(info[i]);
				}
			}
			String value0="0";
			String value1="1";
			for(int i=3;i>=0;i--){
				value0=cnt[0][i]+","+value0;
				value1=cnt[1][i]+","+value1;
			}
			if(!value0.equals("0,0,0,0,0")){
				output.collect(key, new Text(value0));
			}
			if(!value1.equals("0,0,0,0,1")){
				output.collect(key, new Text(value1));
			}
		}
	}

	public static class SplitReducer extends MapReduceBase
			implements
				Reducer<Text, Text, Text, Text> {
		public int max(int a, int b) {
			return a < b ? b : a;
		}
		public void reduce(Text key, Iterator<Text> values,
				OutputCollector<Text, Text> output, Reporter reporter)
				throws IOException {

			int cnt[][] = new int[2][4];
			for (int i = 0; i < 2; i++) {
				for (int j = 0; j < 4; j++) {
					cnt[i][j] = 0;
				}
			}
			while (values.hasNext()) {
				String info[] = values.next().toString().split(",");
				int id = Integer.parseInt(info[4]);
				for (int i = 0; i < 4; i++) {
					cnt[id][i] += Integer.parseInt(info[i]);
				}
			}
			int call = max(cnt[0][0], cnt[1][1]) + max(cnt[0][1], cnt[1][0]);
			int message = max(cnt[0][2], cnt[1][3]) + max(cnt[0][3], cnt[1][2]);
			output.collect(key, new Text(call + "," + message));
		}
	}

	public static void main(String[] args) throws Exception {

		JobConf conf = new JobConf(SplitByMonth.class);
		conf.setJobName("SplitMonth"); // 设置一个用户定义的job名称
		conf.setOutputKeyClass(Text.class); // 为job的输出数据设置Key类
		conf.setOutputValueClass(Text.class); // 为job输出设置value类
		conf.setMapperClass(SplitMapper.class); // 建边
		conf.setCombinerClass(SplitCombiner.class);//为job设置Combiner类
		conf.setReducerClass(SplitReducer.class); // 为job设置Reduce类
		conf.setInputFormat(TextInputFormat.class); // 为map-reduce任务设置InputFormat实现类
		conf.setOutputFormat(TextOutputFormat.class); // 为map-reduce任务设置OutputFormat实现类
		FileInputFormat.setInputPaths(conf, new Path(args[0]));
		FileOutputFormat.setOutputPath(conf, new Path(args[1]));
		JobClient.runJob(conf); // 运行一个job

	}
}