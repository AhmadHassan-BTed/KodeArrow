import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
from dateutil.relativedelta import relativedelta

# Initialize Firebase
def initialize_firestore():
    cred = credentials.Certificate({
        "type": "service_account",
        "project_id": "kodearrow-server",
        "private_key_id": "12f26b7c63d80d9d0901d9b8644b4f5ad12ebb28",
        "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQDGDu+3E6sI34Qw\nqAMOgp0D6fCmNtJmK0ESBFJyUrU38H6ZwtfnSHppnfFvvqbDXiqCCEKvc2dcXBmt\nBndUsXMPNsPv4fLJB30l8EQozr/ai1SsGoHFcZIYXwT0R6Ao5nWy49Ixj+URoBcy\nqfowR60JJMwn+a4KomEEd551f3RIWe/Ik/Oae0Hk3ONTdUGpZpHrN2WxCXSgk3zt\n2FiTZW+HEHyYYAF65XcX94asXpX1UeUMrpf02S8sI2/X/6PUEdGK5YfWhEE35uLH\n4oL62RSIk5b4eoJPC67+rDIDxeBUs3V/LJIn8AoxcW/FWMb1fwdZtZSW/yDqXV4L\nFGYWFwevAgMBAAECggEAFdw5LiJQGuscuogYykW1UeTEyHu9jkRQ6s2qUe76DIIR\nXyRH00HHLRgfOV+4JVEj7PU/cwEQU/vgY54WlrT9R50aVERCmVinwgO6aiyjtVny\njwpf72yBHQqDz/iF323MaOHHZewFcwQR+2gScri+iwdSN0lSId9ZSPZw+XQHYCLG\n/SA+3KXiQlfoHoVi+ZNbzwqJKAwDP5hy0UsvElkULXZLCA31zZZHd9gbhKv8osJa\ngXKbqA/IBF24v+hoO0r3KGj5m+OqEHD7FcGKs5EAxBzLT01dPmPSlDghDkH78HlM\nc6XyHuQaxI6FkBG/FtK/Dy5+fpe3fzAOlxe/vVjYUQKBgQD/2vvNfwEbwggqtweV\n84GAyj7R5x+OYP1Wy5E7fZ4zcoMDxGbm5LUjt3asO8YKxUtB8bSk5HvUcmoLLKfc\nLJy1fu0gv+Xi50lAcDsSrRbpPzy+6feVqh23O5EAZj4ZndhVfyUChALVxK+V1E/a\nfZh4jHqtEOq45Dr/RCApPytckQKBgQDGK5dDtzA4fvKTHfDvidtSILGBYe3jXDX1\nqFIbdLoIcYsQzUjTrepbH4pp55Rx9n+YBHIvs0DhMB2v2kiKCBFPGj7voZbHWfCN\n17qs1gYbmq7dJkm2oPajwqgOuVQZOsjmvVJDAdQNzsMV9hW2Pz7hQ9c8xv8vs+bQ\nsfSLXldAPwKBgDBS0eA8Lp9phFVdAGfH+Bu1FyxZ9NHVa8Pq6uFLloetByW9AJp3\nc+btDdL17y+1l8M6vZ2vMdwsR+8YXhPtsSNud6cJ14eFm4Y6LE4Ytw0SzoxYcFSq\nLrae34ItzWjVMTjkrL7O5CIv5eHsmbBwrE2IatspKMwG/0WbPl/L+IqhAoGAd99I\nadq23YXVAC7dXlh6hYxnM0dkmeJedZHy0M7j9VWRdIFo6zrJh4Nlu7gssF8WQYN2\n+umodk8ftg8JUA2fQsUyisupJD+AZpy3O/Ne0HXaDsYpUsK9TsPh2r46Y+SOQB0H\nVKcXeZ63nWI1Mf/B7ouV+Bq7pERje5wZu/A+QQsCgYAdpDWyLpkSX0SpmUIyL7RC\nUqwhhJ1y1hzh91Gqs9KPz53VzoBHcXT8VmTE4DJG8Nrm3RAxgu0ydmz5n9Fq4BUX\n7E/GIEzKaswgiDUkPHjJzDVF2hs2/5jqopCBK31PxH7jst0r7Xg02AYbSyU/pMqa\ndKmjzfzBS7WlXg06wn0JxA==\n-----END PRIVATE KEY-----\n",
        "client_email": "firebase-adminsdk-9qxya@kodearrow-server.iam.gserviceaccount.com",
        "client_id": "102780777134400554469",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-9qxya%40kodearrow-server.iam.gserviceaccount.com",
        "universe_domain": "googleapis.com"
        }
        )
    
      # cred = credentials.Certificate({
        #     "type": "service_account",
        #     "project_id": "kodearrow-server",
        #     "private_key_id": "d2f88510eb7335c71b35124c039eecb9bd4434d1",
        #     "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC99K1a6/W9q/K6\nlm2Kbj7ambAFIewI/Jgb3U4aOJxWTETmD8+yHC/ZjVq/fvetawiqwlwv66CeAfRa\nsSKij182e/f29bR0t3HefJ6HD7H3ctwnGyed0dr+SNyks/GT9f7YOaYJEMu+R4NY\nUC8pUtZs2xGdOYdIZNOdWtjQ/XgyMOctpUwOc33RluprVREp82BPfwQBvUnCArj6\n2xikrRBmyTSj9lWKB1C/yCV6ujTC4K6l3cQ8qUrOgaSy5niCTKKJfdK4QH8orqvI\noutIDeGFTsohZcAcO1KKjvc+kgTh1W02Ec98dz+CIzraOQmtQMUfU3byrdqarb8y\nf7aSuT7bAgMBAAECggEAWTLIpr3PrunL+NdDh/Id/LuXfsl/k3a9nLQOhVyY+SMm\nZVv+XTZEN+XbO7oM5vewYbMT5ALC8P+c9WthhrFJdgW/mk2ll/s+csnVDToPCVH7\n1Dc5oq/VJHwldAf1hFPLAFENyQsEiYz+Pd2lT8PQ4dv7CPfnMVT7U9RBpN2pb/Nc\nWNNf6YlWsUoSmYRz6GGvYvItOVJlQh47Q2Kx/X0hqmX3FD8/4JgrQZYT6R4g4E1o\neYFpK+XSR5+N13xbR9ZN1MifQT31F43cNhirGhTq1jzC71oX7kUaNhReRUGGGU6F\nzpzTshulwIlMkvC/wWMU+ut4kCrWpDwShv9NB3z95QKBgQDqMN1CIJ+JC7SH7V2x\ngS/IBGz9o1smXVLpVWXcJtOeUbvm3kZXXHviu5ZtRV9k+qSOz7iGUTewZyM508br\npR9MiBdnMTHlgInaQe40xT+hjfzlyNntFwfTCpv0Z/bloEFxsXHgT3HNe5dfRJo2\nU8HpTddSvmTJTHXzAzUUMmUkXQKBgQDPpT5BmQBYqD9HePqX9OHkoKfR+WHjVgRc\nswNvX/J/+ViKlVmDDlQsw2s51LvxjD9LrAVq7c96DrX4hAqgdw/MqTC3CVHrb8cN\nrZzmPJjDGUzqgT2MXh0t8WbILcg8JNHZ1+WP9kUL1rKL6UtVpo9nyWD+b89PaVJ/\nf9ZrXgc8lwKBgHJICCDV5KQu5xkRtxAA171Gk50uUzOkhOpCdyN4evoeLpCZ1T+a\nbQYWvnByUvvm59ic+xHonkFiAymb881YVa62Fp2PvyaclCjC1ahAvS1sKYZEfjwZ\nagMNgU9CUJR7oJQHoGdyvTkl35do1cw/ETh1eOby7CHjQwekgAlsEjktAoGBAJQt\np6/IL6cU6ZNnkey+pDUzMI93F5PT3mkIlnr0TWll1vmOesI7h3YqPmqWlUhafRDT\nQUp9SoIf3VvrXmoEjRHP6yOzUvJgYfww2La0p48SjwEKGZIB13DhxCc2BJ5m6Bo9\nJ2UEqWE5ZVDSux/0LII0AzOPNrHEx0qVP75+60shAoGAO2AMVM4c1d1DrfGeUThF\nDrLfoNrRpMGQvi704hN7q3nbbza/ku6f+1c3XmOKNgTsSpOb1rVhm91c1Vozhu8Y\nqvRaTz2KRwxd4v6tJhLyfisP5CwxHi+/sLtL9Pb9H+bBeoJEBA49oE3hbyj+utjm\nU5XhilsACK0pg84K7ueKgjo=\n-----END PRIVATE KEY-----\n",
        #     "client_email": "firebase-adminsdk-9qxya@kodearrow-server.iam.gserviceaccount.com",
        #     "client_id": "102780777134400554469",
        #     "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        #     "token_uri": "https://oauth2.googleapis.com/token",
        #     "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        #     "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-9qxya%40kodearrow-server.iam.gserviceaccount.com",
        #     "universe_domain": "googleapis.com"
        #     })
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    return db
    
db = initialize_firestore()

def add_user(email, subscription_date_str):

    subscription_date = datetime.strptime(subscription_date_str, "%Y-%m-%d").date()

    # Convert subscription_date to string
    subscription_date_str = subscription_date.strftime("%Y-%m-%d")

    # Add the email to Firestore users collection if it doesn't already exist
    doc_ref_user = db.collection('ControlGroup').document(email)
    doc_user = doc_ref_user.get()
    if doc_user.exists:
        print(f"Email '{email}' already exists in Firestore users collection.")
    else:
        # Add the email and subscription date to Firestore users collection
        doc_ref_user.set({'email': email, 'subscription_date': subscription_date_str})
        
        # Initialize additional user usage variables
        usage_data = {
            'charactersTyped': 0,
            'kodeArrowHotkeys': 0,
            'TotalUsageMinutes': 0
        }
        doc_ref_user.collection('usage').document('usage_data').set(usage_data)
        
        print(f"Added '{email}' to users collection with subscription date {subscription_date_str}.")
        print("Initialized user usage variables: charactersTyped, kodeArrowHotkeys, TotalUsageMinutes.")

if __name__ == "__main__":

    user_email = "rp01@kodeArrow.com"
    subscription_period = 3
    
    subscription_date = datetime.today()  # Today's date as a datetime object
    subscription_date_str = datetime.today().strftime("%Y-%m-%d")  # Use today's date as a string

    subscription_expiration_date = subscription_date + relativedelta(months=subscription_period)
    subscription_expiration_date_str = subscription_expiration_date.strftime("%Y-%m-%d")
    add_user(user_email, subscription_expiration_date_str)

    
