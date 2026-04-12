import sqlite3
import json
import random

DATABASE = 'ciliAI/fangtang.db'

def add_ip_works():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ip_works (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            student_name TEXT,
            image TEXT,
            tags TEXT,
            cost TEXT,
            duration TEXT,
            price TEXT,
            copyright TEXT,
            introduction TEXT,
            status TEXT DEFAULT 'active',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    ip_works = [
        {
            'title': '鏄熼檯绌胯秺鑰?,
            'student_name': 'CiliAI瀹樻柟',
            'image': 'https://picsum.photos/400/600?random=1001',
            'tags': ['绉戝够', '鍐掗櫓', 'AI鐢熸垚'],
            'cost': '150',
            'duration': '180',
            'price': '299',
            'copyright': '鐣寗灏忚',
            'introduction': '璁茶堪浜虹被鍦ㄥ畤瀹欎腑瀵绘壘鏂板鍥殑鍙茶瘲鏁呬簨銆?
        },
        {
            'title': '鏃跺厜鏃呰鑰?,
            'student_name': '鏂瑰瀹樻柟',
            'image': 'https://picsum.photos/400/600?random=1002',
            'tags': ['鎮枒', '绌胯秺', 'AI鐢熸垚'],
            'cost': '140',
            'duration': '160',
            'price': '259',
            'copyright': '鐣寗灏忚',
            'introduction': '涓€涓櫘閫氫汉鎰忓鑾峰緱绌胯秺鏃剁┖鐨勮兘鍔涳紝鏀瑰彉鍛借繍鐨勬晠浜嬨€?
        },
        {
            'title': '閮藉競鐚庝汉',
            'student_name': '鏂瑰瀹樻柟',
            'image': 'https://picsum.photos/400/600?random=1003',
            'tags': ['鍔ㄤ綔', '閮藉競', 'AI鐢熸垚'],
            'cost': '135',
            'duration': '150',
            'price': '249',
            'copyright': '鐣寗灏忚',
            'introduction': '鐜颁唬閮藉競涓殑绁炵鐚庝汉锛岄潰瀵归粦鏆楀娍鍔涚殑鎸戞垬銆?
        },
        {
            'title': '淇粰涔嬭矾',
            'student_name': '鏂瑰瀹樻柟',
            'image': 'https://picsum.photos/400/600?random=1004',
            'tags': ['鐜勫够', '淇粰', 'AI鐢熸垚'],
            'cost': '160',
            'duration': '200',
            'price': '399',
            'copyright': '鐣寗灏忚',
            'introduction': '涓€涓钩鍑″皯骞寸殑淇粰涔嬫梾锛屽巻缁忕（闅剧粓鎴愬ぇ閬撱€?
        },
        {
            'title': '鐖辨儏鍏瘬',
            'student_name': '鏂瑰瀹樻柟',
            'image': 'https://picsum.photos/400/600?random=1005',
            'tags': ['鐖辨儏', '鍠滃墽', 'AI鐢熸垚'],
            'cost': '120',
            'duration': '140',
            'price': '199',
            'copyright': '鐣寗灏忚',
            'introduction': '涓€缇ゅ勾杞讳汉鍦ㄥ叕瀵撻噷鐨勬涔愭棩甯稿拰鐖辨儏鏁呬簨銆?
        },
        {
            'title': '鐩楀绗旇',
            'student_name': '鏂瑰瀹樻柟',
            'image': 'https://picsum.photos/400/600?random=1006',
            'tags': ['鎺㈤櫓', '鎮枒', 'AI鐢熸垚'],
            'cost': '145',
            'duration': '170',
            'price': '279',
            'copyright': '鐣寗灏忚',
            'introduction': '娣卞叆鍙ゅ锛屾帰绱㈡湭鐭ヤ笘鐣岀殑鍐掗櫓鏁呬簨銆?
        },
        {
            'title': '瀹环鍓?,
            'student_name': '鏂瑰瀹樻柟',
            'image': 'https://picsum.photos/400/600?random=1007',
            'tags': ['鍙ら', '瀹枟', 'AI鐢熸垚'],
            'cost': '155',
            'duration': '185',
            'price': '329',
            'copyright': '鐣寗灏忚',
            'introduction': '鍙や唬瀹环涓殑鏉冭皨涓庣埍鎯咃紝绮惧僵鐨勫鏂楀ぇ鎴忋€?
        },
        {
            'title': '鏈潵涓栫晫',
            'student_name': '鏂瑰瀹樻柟',
            'image': 'https://picsum.photos/400/600?random=1008',
            'tags': ['绉戝够', '璧涘崥鏈嬪厠', 'AI鐢熸垚'],
            'cost': '165',
            'duration': '195',
            'price': '359',
            'copyright': '鐣寗灏忚',
            'introduction': '2088骞寸殑鏈潵涓栫晫锛岄珮绉戞妧涓庝汉绫绘儏鎰熺殑纰版挒銆?
        },
        {
            'title': '姝︿緺椋庝簯',
            'student_name': '鏂瑰瀹樻柟',
            'image': 'https://picsum.photos/400/600?random=1009',
            'tags': ['姝︿緺', '鍔ㄤ綔', 'AI鐢熸垚'],
            'cost': '148',
            'duration': '175',
            'price': '289',
            'copyright': '鐣寗灏忚',
            'introduction': '姹熸箹鎭╂€紝鍒€鍏夊墤褰憋紝涓€浠ｆ渚犵殑浼犲鏁呬簨銆?
        },
        {
            'title': '鏍″洯闈掓槬',
            'student_name': '鏂瑰瀹樻柟',
            'image': 'https://picsum.photos/400/600?random=1010',
            'tags': ['闈掓槬', '鏍″洯', 'AI鐢熸垚'],
            'cost': '110',
            'duration': '130',
            'price': '179',
            'copyright': '鐣寗灏忚',
            'introduction': '闈掓槬娲嬫孩鐨勬牎鍥敓娲伙紝鍙嬫儏涓庣埍鎯呯殑缇庡ソ鏃跺厜銆?
        },
        {
            'title': '鐮存楂樻墜',
            'student_name': '鏂瑰瀹樻柟',
            'image': 'https://picsum.photos/400/600?random=1011',
            'tags': ['鍒戜睛', '鎮枒', 'AI鐢熸垚'],
            'cost': '138',
            'duration': '158',
            'price': '269',
            'copyright': '鐣寗灏忚',
            'introduction': '澶╂墠渚︽帰鐮磋В涓€涓張涓€涓鎵嬬殑妗堜欢銆?
        },
        {
            'title': '鍟嗘垬绮捐嫳',
            'student_name': '鏂瑰瀹樻柟',
            'image': 'https://picsum.photos/400/600?random=1012',
            'tags': ['鍟嗘垬', '鑱屽満', 'AI鐢熸垚'],
            'cost': '142',
            'duration': '165',
            'price': '259',
            'copyright': '鐣寗灏忚',
            'introduction': '鍟嗗満濡傛垬鍦猴紝绮捐嫳浠殑鏅烘収涓庤儐璇嗚緝閲忋€?
        }
    ]

    for work in ip_works:
        try:
            cursor.execute('''
                INSERT INTO ip_works (title, student_name, image, tags, cost, duration, price, copyright, introduction)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                work['title'],
                work['student_name'],
                work['image'],
                json.dumps(work['tags']),
                work['cost'],
                work['duration'],
                work['price'],
                work['copyright'],
                work['introduction']
            ))
            print(f"鉁?娣诲姞浣滃搧: {work['title']}")
        except Exception as e:
            print(f"鉁?娣诲姞浣滃搧澶辫触 {work['title']}: {e}")

    conn.commit()
    conn.close()
    print("\n鎴愬姛娣诲姞 IP 鐗堟潈浣滃搧锛?)

if __name__ == '__main__':
    add_ip_works()

