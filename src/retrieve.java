import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileInputStream;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;

class Node{
	double score;
	String id;
}
public class retrieve {
	public static double stopWordSize = 0.0;
	public static HashMap<String, List<String>> word_dict = null;
	public static HashMap<String, List<String>> iterm_vect = null;
	public static HashMap<String, String> readin(String fileName) throws IOException{
		
		HashMap<String, String> map = new HashMap<String, String>();
		BufferedReader br = new BufferedReader(new InputStreamReader(new FileInputStream(fileName)));
		
		String line = null;
		while((line = br.readLine()) != null){
			String[] parts = line.split("\t");
			map.put(parts[0], parts[3].toLowerCase());
		}
		return map;
	}
	public static HashMap<String, List<String>> toWordDict(HashMap<String, String> iterms){
		word_dict = new HashMap<String, List<String>>();
		for(String key : iterms.keySet()){
			String[] words = iterms.get(key).split("[( )]");
			for(String word : words){
				if(word.equals("-") || word.length() == 0 || word.equals("+"))
					continue;
				if(word_dict.containsKey(word)){
					List<String> cur = word_dict.get(word);
					cur.add(key);
				}
				else{
					List<String> cur = new ArrayList<String>();
					cur.add(key);
					word_dict.put(word, cur);
				}
			}
		}
		stopWordSize = (double)word_dict.size() / 5.0;
//		System.out.println("voc size:" + word_dict.size());
		return word_dict; 
	}
	public static HashMap<String,Double> get_set(String a){
		HashMap<String,Double> result = new HashMap<String,Double>();
		String[] aWords = a.split(" ");
		for(String x : aWords){
			if(result.containsKey(x))
				result.put(x, result.get(x)+1.0);
			else
				result.put(x, 1.0);
		}
		return result;
	}
	public static double compute_cos(String a, String b){
		HashMap<String,Double> as = get_set(a);
		HashMap<String,Double> bs = get_set(b);
		double dot = 0.0;
		double accumA = 0.0;
		for(String word : as.keySet()){
			if(bs.containsKey(word)){
				dot += as.get(word) * bs.get(word);
			}
			accumA += as.get(word) * as.get(word);
		}
		double accumB = 0.0;
		for(String word : bs.keySet()){
			accumB += bs.get(word) * bs.get(word);
		}
	
		return dot / (Math.sqrt(accumA) * Math.sqrt(accumB));
	}
	public static void put(HashMap<String, Double> scores10, double cos, String cand){
		if(scores10.size() < 10)
			scores10.put(cand, cos);
		else{
			double min = Double.MAX_VALUE;
			String rem = null;
			for(String key : scores10.keySet()){
				if(scores10.get(key) < min){
					min = scores10.get(key);
					rem = key;
				}
			}
			scores10.remove(rem);
			scores10.put(cand, cos);
		}
		return;
	}
	public static List<String> trans2List(HashMap<String, Double> scores10){
		if(scores10.size() > 10)
			System.out.println("error 1");
		List<String> res = new ArrayList<String>();
		for(String w : scores10.keySet()){
			res.add(w);
		}
		return res;
	}
	public static HashMap<String, List<String>> retrie(HashMap<String, List<String>> word_dict, HashMap<String, String> iterms){
		HashMap<String, List<String>> top10s = new HashMap<String, List<String>>();
		HashSet<String> curList = null;
		for(String index : iterms.keySet()){
			//get all titles share words with cur title
			System.out.println("cur index:" + index);
			curList = new HashSet<String>();
			String[] words = iterms.get(index).split(" ");
			for(String word : words){
				if(word_dict.get(word).size() > stopWordSize)
					continue;
				System.out.print(word+":"+word_dict.get(word).size() + " ");
				for(String ids : word_dict.get(word)){
					curList.add(ids);
				}
			}
			System.out.println("\nlist size:" + curList.size());
			//compute top 10 titles
			HashMap<String, Double> scores10 = new HashMap<String, Double>();
			for(String candidate : curList){
				double cosine = compute_cos(iterms.get(index), iterms.get(candidate));
				put(scores10, cosine, candidate);
			}
//			System.out.println("to");
			//put it into top10s stirng
			List<String> top10 = trans2List(scores10); 
			top10s.put(index, top10);	
		}
		return top10s;
	}
	public static void output(HashMap<String, List<String>> top10s) throws IOException{
		FileWriter fw = new FileWriter("laptops.txt");
		BufferedWriter bw = new BufferedWriter(fw);
		for(String key : top10s.keySet()){
			bw.write(key + "\t");
			for(String cand : top10s.get(key)){
				bw.write(cand + " ");
			}
			bw.write("\n");
		}
		bw.flush();
		bw.close();
		return;
	}
	public static void main(String[] args) throws IOException{
		HashMap<String, String> iterms = readin(args[0]);
		HashMap<String, List<String>> word_dict = toWordDict(iterms);
		HashMap<String, List<String>> top10s = retrie(word_dict, iterms);
		output(top10s);
	}
}
