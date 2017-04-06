import pymysql;
import config as config

class DbHandler:
    def __init__(self):
        self.user='root';
        self.password='ntstha';
        self.host='127.0.0.1';
        self.database='Amazon';


    def getConnection(self):
        cnx = pymysql.connect(user=self.user, password=self.password,
                                   host=self.host,
                                   database=self.database);
        return cnx;

    def closeConnection(self,cnx):
        cnx.close();

    def insert_reviews_toDb(self,review_dict_list,table_name):
        try:
            cnx = self.getConnection();
            cur = cnx.cursor();
            sql = "INSERT INTO %s ( `rating`, `product_id`, `helpfulness`,`ID`,`review_by`, `title`, `review_time`,`review` ) VALUES ( %(rating)s, %(product_id)s, %(helpfulness)s, %(id)s,%(review_by)s,%(title)s,%(review_time)s,%(review)s)"%table_name;
            cur.executemany(sql, review_dict_list);
            cnx.commit();
        finally:
            cur.close();
            self.closeConnection(cnx);

    def selectAllFromTable(self,table_name):
        try:
            cnx = self.getConnection();
            cur = cnx.cursor(pymysql.cursors.DictCursor);
            sql = "SELECT * FROM %s"%table_name;
            cur.execute(sql);
            result = cur.fetchall();
            cnx.commit();
            return result;
        finally:
            cur.close();
            self.closeConnection(cnx);

    def getIdAndRatingFromTable(self,table_name):
        try:
            cnx = self.getConnection();
            cur = cnx.cursor(pymysql.cursors.DictCursor);
            sql="select prm_id,rating from %s"%table_name;
            cur.execute(sql);
            result = cur.fetchall();
            cnx.commit();
            return result;
        finally:
            cur.close();
            self.closeConnection(cnx);

    def getUniformSample(self,table_name):
        try:
            cnx = self.getConnection();
            cur = cnx.cursor(pymysql.cursors.DictCursor);
            sql="(select * from %s where rating=5 order by Rand() limit 0,2000) " \
                "union (select * from %s where rating=4 order by Rand() limit 0,2000) " \
                "union (select * from %s where rating=3 order by Rand() limit 0,2000) " \
                "union (select * from %s where rating=2 order by Rand() limit 0,2000) " \
                "union (select * from %s where rating=1 order by Rand() limit 0,2000)"%(table_name,table_name,table_name,table_name,table_name);

            cur.execute(sql);
            result = cur.fetchall();
            cnx.commit();
            return result;
        finally:
            cur.close();
            self.closeConnection(cnx);

    def getIdRatingFromUniformSample(self,table_name):
        try:
            cnx = self.getConnection();
            cur = cnx.cursor(pymysql.cursors.DictCursor);
            sql="(select prm_id,rating from %s where rating=5 order by Rand() limit 0,2000) " \
                "union (select prm_id,rating from %s where rating=4 order by Rand() limit 0,2000) " \
                "union (select prm_id,rating from %s where rating=3 order by Rand() limit 0,2000) " \
                "union (select prm_id,rating from %s where rating=2 order by Rand() limit 0,2000) " \
                "union (select prm_id,rating from %s where rating=1 order by Rand() limit 0,2000)"%(table_name,table_name,table_name,table_name,table_name);

            cur.execute(sql);
            result = cur.fetchall();
            cnx.commit();
            return result;
        finally:
            cur.close();
            self.closeConnection(cnx);


    def getIdRatingGroupedByProduct(self,table_name):
        try:
            cnx = self.getConnection();
            cur = cnx.cursor(pymysql.cursors.DictCursor);
            sql="select * from Review_10m order by product_id asc;";
            cur.execute(sql);
            result = cur.fetchall();
            cnx.commit();
            return result;
        finally:
            cur.close();
            self.closeConnection(cnx);

    def getReviewGroupedByProductOrderByTime(self,table_name):
        try:
            cnx = self.getConnection();
            cur = cnx.cursor(pymysql.cursors.DictCursor);
            sql="select * from %s as r order by r.product_id,r.review_time asc;"%table_name;
            cur.execute(sql);
            result = cur.fetchall();
            cnx.commit();
            return result;
        finally:
            cur.close();
            self.closeConnection(cnx);

    def getLatestReviewForUniqueProduct(self,table_name):
        try:
            cnx = self.getConnection();
            cur = cnx.cursor(pymysql.cursors.DictCursor);
            sql="select r.prm_id,r.product_id from %s r left join (select * from %s as r order by r.product_id,r.review_time asc) as temp on (r.product_id=temp.product_id and r.review_time<temp.review_time) where temp.prm_id is null"%(table_name,table_name);
            cur.execute(sql);
            result = cur.fetchall();
            cnx.commit();
            return result;
        finally:
            cur.close();
            self.closeConnection(cnx);

