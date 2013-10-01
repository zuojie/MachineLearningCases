import org.apache.mahout.cf.taste.common.Refreshable;
import org.apache.mahout.cf.taste.common.TasteException;
import org.apache.mahout.cf.taste.impl.model.file.*;
import org.apache.mahout.cf.taste.impl.neighborhood.*;
import org.apache.mahout.cf.taste.impl.recommender.*;
import org.apache.mahout.cf.taste.impl.recommender.slopeone.SlopeOneRecommender;
import org.apache.mahout.cf.taste.impl.similarity.*;
import org.apache.mahout.cf.taste.model.*;
import org.apache.mahout.cf.taste.neighborhood.*;
import org.apache.mahout.cf.taste.recommender.*;
import org.apache.mahout.cf.taste.similarity.*;

import com.sun.org.apache.xalan.internal.xsltc.runtime.Hashtable;

import java.io.*;
import java.util.*;

public class DianPingRecommender {
	private DianPingRecommender() {
	};

	static Hashtable user_id2name = new Hashtable();
	static Hashtable item_id2name = new Hashtable();

	public static void initID2Name(Hashtable res, String fin) {
		//FileReader reader = null;
		FileInputStream fis = null;
		InputStreamReader isr = null;
		BufferedReader br = null;
		try {
			//reader = new FileReader(fin);
			fis = new FileInputStream(fin);
			// 中文乱码（文件为UTF8格式，eclipse默认编码GBK）
			isr = new InputStreamReader(fis, "UTF-8");
			br = new BufferedReader(isr);
			String line = null;
			String[] items;
			while (null != (line = br.readLine())) {
				items = line.split("\t");
				//res.put(Long.valueOf(items[0]), new String(items[1].getBytes("GBK"), "UTF-8"));
				res.put(Long.valueOf(items[0]), items[1]);
				
			}
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		} finally {
			try {
				if (br != null) {
					br.close();
				}
				if (isr != null) {
					isr.close();
				}
				if (fis != null) {
					fis.close();
				}
			} catch (IOException e) {
				e.printStackTrace();
			}
		}
	}
	// User Based Collaborative Filtering
	class UserBasedRecommender implements Recommender {
		private Recommender recommender;
		public UserBasedRecommender(DataModel model, UserSimilarity user_similarity, int knn)
						throws IOException, TasteException {
			user_similarity.setPreferenceInferrer(new AveragingPreferenceInferrer(model));
			UserNeighborhood neighborhood = 
	            new NearestNUserNeighborhood(knn, user_similarity, model); 
	        recommender = new CachingRecommender( 
	            new GenericUserBasedRecommender(model, neighborhood, user_similarity)); 
		}
		@Override
		public float estimatePreference(long userID, long itemID)
				throws TasteException {
			return recommender.estimatePreference(userID, itemID);
		}
		@Override
		public DataModel getDataModel() {
			return recommender.getDataModel();
		}
		@Override
		public List<RecommendedItem> recommend(long userID, int howMany)
				throws TasteException {
			return recommender.recommend(userID, howMany);
		}
		@Override
		public List<RecommendedItem> recommend(long userID, int howMany,
				IDRescorer rescorer) throws TasteException {
			return recommender.recommend(userID, howMany, rescorer);
		}
		@Override
		public void removePreference(long userID, long itemID)
				throws TasteException {
			recommender.removePreference(userID, itemID);
		}
		@Override
		public void setPreference(long userID, long itemID, float value)
				throws TasteException {
			recommender.setPreference(userID, itemID, value);
		}
		@Override
		public void refresh(Collection<Refreshable> alreadyRefreshed) {
			recommender.refresh(alreadyRefreshed);
		}
	}
	// Item Based Collaborative Filtering
	class ItemBasedRecommender implements Recommender {
		private Recommender recommender;
		public ItemBasedRecommender(DataModel model, ItemSimilarity item_similarity)
						throws IOException, TasteException {
	        recommender = new CachingRecommender( 
	            new GenericItemBasedRecommender(model, item_similarity)); 
		}
		@Override
		public float estimatePreference(long userID, long itemID)
				throws TasteException {
			return recommender.estimatePreference(userID, itemID);
		}
		@Override
		public DataModel getDataModel() {
			return recommender.getDataModel();
		}
		@Override
		public List<RecommendedItem> recommend(long userID, int howMany)
				throws TasteException {
			return recommender.recommend(userID, howMany);
		}
		@Override
		public List<RecommendedItem> recommend(long userID, int howMany,
				IDRescorer rescorer) throws TasteException {
			return recommender.recommend(userID, howMany, rescorer);
		}
		@Override
		public void removePreference(long userID, long itemID)
				throws TasteException {
			recommender.removePreference(userID, itemID);
		}
		@Override
		public void setPreference(long userID, long itemID, float value)
				throws TasteException {
			recommender.setPreference(userID, itemID, value);
		}
		@Override
		public void refresh(Collection<Refreshable> alreadyRefreshed) {
			recommender.refresh(alreadyRefreshed);
		}
	}
	// SlopeOne 
	class MySlopeOneRecommender implements Recommender {
		private Recommender recommender;
		public MySlopeOneRecommender(DataModel model)
						throws IOException, TasteException {
	        recommender = new CachingRecommender( 
	            new SlopeOneRecommender(model)); 
		}
		@Override
		public float estimatePreference(long userID, long itemID)
				throws TasteException {
			return recommender.estimatePreference(userID, itemID);
		}
		@Override
		public DataModel getDataModel() {
			return recommender.getDataModel();
		}
		@Override
		public List<RecommendedItem> recommend(long userID, int howMany)
				throws TasteException {
			return recommender.recommend(userID, howMany);
		}
		@Override
		public List<RecommendedItem> recommend(long userID, int howMany,
				IDRescorer rescorer) throws TasteException {
			return recommender.recommend(userID, howMany, rescorer);
		}
		@Override
		public void removePreference(long userID, long itemID)
				throws TasteException {
			recommender.removePreference(userID, itemID);
		}
		@Override
		public void setPreference(long userID, long itemID, float value)
				throws TasteException {
			recommender.setPreference(userID, itemID, value);
		}
		@Override
		public void refresh(Collection<Refreshable> alreadyRefreshed) {
			recommender.refresh(alreadyRefreshed);
		}
	}
	
	public static void main(String args[]) throws Exception {
		initID2Name(user_id2name, "E:\\dev\\jitizhihui\\dianping\\data\\dianping_huoguo_userid.txt");
		initID2Name(item_id2name, "E:\\dev\\jitizhihui\\dianping\\data\\dianping_huoguo_itemid.txt");
		String f_path = "E:\\dev\\jitizhihui\\dianping\\data\\dianping_huoguo_userid_based.txt";
		String f_path_sample = "E:\\dev\\jitizhihui\\dianping\\data\\dianping_huoguo_userid_based_sample.txt";
		DataModel model = new FileDataModel(new File(f_path));// 文件名一定要是绝对路径
		DianPingRecommender master = new DianPingRecommender();
		long user_id = 3;
		List<RecommendedItem> recommendations = null;
		//PearsonCorrelationSimilarity：基于皮尔逊相关系数计算相似度
		//EuclideanDistanceSimilarity：基于欧几里德距离计算相似度
		//TanimotoCoefficientSimilarity：基于 Tanimoto 系数计算相似度
		//UncerteredCosineSimilarity：计算 Cosine 相似度
		//UserSimilarity similarity_u = new PearsonCorrelationSimilarity(model);
		UserSimilarity similarity_u = new EuclideanDistanceSimilarity(model);
		int knn = 20;
		String shop;
		Recommender recommender = null;
		// User Based
		recommender = master.new UserBasedRecommender(model, similarity_u, knn);
		recommendations = recommender.recommend(user_id, knn);// 为用户user_id推荐knn个ItemID
		System.out.println("[User CF]为用户" + user_id2name.get(user_id) + "推荐的结果");
		for(RecommendedItem recommendation : recommendations) {
			shop = (String) item_id2name.get(recommendation.getItemID());
			System.out.println(shop + ":" + recommendation.getValue());
		}
		System.out.println("-----------");
		// Item Based
		//ItemSimilarity similarity_i = new PearsonCorrelationSimilarity(model);
		ItemSimilarity similarity_i = new EuclideanDistanceSimilarity(model);
		recommender = master.new ItemBasedRecommender(model, similarity_i);
		recommendations = recommender.recommend(user_id, knn);// 为用户1推荐20个ItemID
		System.out.println("[Item CF]为用户" + user_id2name.get(user_id) + "推荐的结果");
		for(RecommendedItem recommendation : recommendations) {
			shop = (String) item_id2name.get(recommendation.getItemID());
			System.out.println(shop + ":" + recommendation.getValue());
		}
		System.out.println("-----------");
		// SlopeOne
		recommender = master.new MySlopeOneRecommender(model);
		recommendations = recommender.recommend(user_id, knn);// 为用户1推荐20个ItemID
		System.out.println("[SlopeOne CF]为用户" + user_id2name.get(user_id) + "推荐的结果");
		for(RecommendedItem recommendation : recommendations) {
			shop = (String) item_id2name.get(recommendation.getItemID());
			System.out.println(shop + ":" + recommendation.getValue());
		}
	}
}