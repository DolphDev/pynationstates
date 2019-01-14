# from nationstates.objects import Auth
# import unittest

# class resp(object):
#     def __init__(self):
#         self.headers = {"X-autologin":2, "X-pin":3}


# class session(object):

#     def __init__(self):
#         self.headers = {}

#     def get(*args, **kwargs):
#         return resp()





# class TestAuth(unittest.TestCase):

#     def test_headers_use_password(self):
#         auth = Auth(1,password=1)
#         self.assertEqual(auth.headers(), {"Password": 1})

#     def test_headers_use_password_then_pin(self):
#         auth = Auth(1,password=1)
#         self.assertEqual(auth.headers(), {"Password": 1})
#         auth.__pin__ = 3
#         self.assertEqual(auth.headers(), {"Pin": 3})
    
#     def test_headers_use_autologin_over_password(self):
#         auth = Auth(1,password=1,autologin=2)
#         self.assertEqual(auth.headers(), {"Autologin": 2})

#     def test_headers_use_autologin_over_password_then_pin(self):
#         auth = Auth(1,password=1,autologin=2)
#         self.assertEqual(auth.headers(), {"Autologin": 2})
#         auth.__pin__ = 3
#         self.assertEqual(auth.headers(), {"Pin": 3})

#     def test_headers_use_autologin_then_pin(self):
#         auth = Auth(1,autologin=2)
#         self.assertEqual(auth.headers(), {"Autologin": 2})
#         auth.__pin__ = 3
#         self.assertEqual(auth.headers(), {"Pin": 3})
        
#     def test_headers_user_usepasswordoral_password(self):
#         auth = Auth(1, password=1, pin=3)
#         auth.__usepasswordoral__ = True
#         self.assertEqual(auth.headers(), {"Password": 1})
    
#     def test_headers_user_usepasswordoral_autologin(self):
#         auth = Auth(1, autologin=2, pin=3)
#         auth.__usepasswordoral__ = True
#         self.assertEqual(auth.headers(), {"Autologin": 2})

#     def test_isauth(self):
#         self.assertFalse(Auth(0).isauth())
#         self.assertTrue(Auth(0,1).isauth())  

#     def test_get_wrapper_password_only(self):
#         auth = Auth(session(), 1)
#         resp = auth.get()
#         print(resp.headers)
#         self.assertTrue((bool(auth.__pin__) and bool(auth.__autologin__)))


