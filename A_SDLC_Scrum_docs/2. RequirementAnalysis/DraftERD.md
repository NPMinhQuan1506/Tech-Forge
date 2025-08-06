# User & Identity
1. MLTF_Guest (ID, Name, Phone, GenderID, Email, IPAddress, Created)
2. MLTF_User (ID, Code, Name, Bio, AliasName, Avatar, Email, GenderID, BirthDay, Phone, Phone2, PhoneCodeID, Address, WardID. DistrictID, CityID, CountryID, NationalID, SchoolID, CareerID, JobTitleID, EducationID, Username, PasswordHash, GoogleID, SourceID, GroupID, TypeID, RankID, AccessFailedCount, LockoutEnd, TwoFactorEnabled, SecurityStamp, LastSignIn, IsLife, DiscoverPoint, Note, Created, Modified, State, Searchable, NumCreated, NumLastModified, NumLastSignIn)
3. MLTF_UserSource (ID, Name, Note, Created, CreatedBy, Modified, ModifiedBy, State)
4. MLTF_UserSource_Detail (ID, ParentID, Name, Note, Created, CreatedBy, Modified, ModifiedBy, State)
5. MLTF_UserType (ID, Name, Note, Created, CreatedBy, Modified, ModifiedBy, State)
6. MLTF_UserOAuth2 (ID, UserID, OAuthSupID, AccessID, AccessToken, Note, Created, CreatedBy, Modified, ModifiedBy, State)
7. MLTF_Topic (ID, Code, Name, Description, VisibleOrder, GroupID, Searchable, Note, Created, CreatedBy, Modified, ModifiedBy, State) **# Core Learning **
8. MLTF_Lesson (ID, Code, Name, Description, Content, TopicID, GroupID, TagID, LevelID, Note, DiscoveryPoint, Created, CreatedBy, Modified, ModifiedBy, State)
9. MLTF_TopicGroup (ID, Name, Note, Created, CreatedBy, Modified, ModifiedBy, State)
10. MLTF_LessonGroup (ID, Name, Note, Created, CreatedBy, Modified, ModifiedBy, State)
11. MLTF_LessonTag (ID, Name, Note, Created, CreatedBy, Modified, ModifiedBy, State)
12. MLTF_LessonLevel (ID, Name, Note, Created, CreatedBy, Modified, ModifiedBy, State)
13. MLTF_ExerciseTemplate (ID, Code, Name, Description, ReferencePoint, LessonID, Note, Created, CreatedBy, Modified, ModifiedBy, State)
14. MLTF_ExerciseTemplate_Detail (ID, ParentID, Name, Description, Content, ItemPoint, Type, Note, Created, CreatedBy, Modified, ModifiedBy, State)
15. MLTF_ExerciseTemplate_TestCase (ID, ExerciseID, Type, Value, ItemPoint, Note, Created, CreatedBy, Modified, ModifiedBy, State)
16. MLTF_ExamTemplate (ID, TopicID, Code, Description, Note, Created, CreatedBy, Modified, ModifiedBy, State)
17. MLTF_ExamTemplate_Detail
18. MLTF_Exam_Answer
19. MLTF_User_TrackingLesson
20. MLTF_RoadMap **# Learning Path**
21. MLTF_RoadMap_Lesson
22. MLTF_RoadMap_Exercise
23. MLTF_RoadMap_Exam
24. MLTF_Course
25. MLTF_Course_Lesson
26. MLTF_Course_Exercise
27. MLTF_Course_Exam
28. MLTF_User_RoadMap **# User Progress**
29. MLTF_User_RoadMap_Detail
30. MLTF_User_RoadMap_Exercise
31. MLTF_User_RoadMap_Submission
32. MLTF_User_RoadMap_Exam
33. MLTF_User_RoadMap_Exam_Detail
34. MLTF_User_Course
35. MLTF_User_Course_Detail
36. MLTF_User_Course_Exercise
37. MLTF_User_Course_Submission
38. MLTF_User_Course_Exam
39. MLTF_User_Course_Exam_Detail
40. MLTF_MemberRank **# Gamification & Community**
41. MLTF_Certificate
42. MLTF_Certificate_RankCondition
43. MLTF_Certificate_Condition
44. MLTF_Reward
45. MLTF_User_RedeemRewards
46. MLTF_User_IssueDiscuss
47. MLTF_User_IssueDiscuss_Detail
48. MLTF_User_RoadMap_Share
49. MLTF_User_RoadMap_ShareRating
50. MLTF_Product **# E-Commerce**
51. MLTF_ProductType
52. MLTF_ProductUnit
53. MLTF_ProductUnit_Redeem
54. MLTF_ProductSource
55. MLTF_Supplier
56. MLTF_Customer_Order
57. MLTF_Customer_Order_Detail
58. MLTF_Customer_Payment
59. MLTF_Customer_Payment_Detail
60. MLTF_Discount
61. MLTF_Discount_Detail
62. MLTF_Customer_Wallet
63. MLTF_Customer_Wallet_Transaction
64.  MLTF_User_Log **# System logs & Auditing**
65.  MLTF_User_LogType
66.  MLTF_MS_Company **# Internal & Admin System**
67.  MLTF_MS_Employee
68.  MLTF_MS_Employee_Group
69.  MLTF_MS_Employee_Department
70.  MLTF_MS_Employee_Role
71.  MLTF_MS_Employee_GroupRole
72.  MLTF_MS_UserAccount
73.  MLTF_MS_SettingClient_Display
74.  MLTF_MS_SettingClient_Option
75. MLTF_MS_Setting_Option
76. MLTF_MS_Menu
77. MLTF_MS_MenuGroup
78. MLTF_MS_UserMenu_Allow
79. MLTF_MS_Control
80. MLTF_MS_UserControl_Block
81.  MLTF_MS_Catalog_Gender **# Master Data / Catalog**
82.  MLTF_MS_Catalog_National
83.  MLTF_MS_Catalog_National
84.  MLTF_MS_Catalog_Country
85.  MLTF_MS_Catalog_City
86.  MLTF_MS_Catalog_Ward
87.  MLTF_MS_Catalog_Street
88.  MLTF_MS_Catalog_Career
89.  MLTF_MS_Catalog_JobTitle
90.  MLTF_MS_Catalog_School
91. MLTF_MS_Catalog_School_Type
92. MLTF_MS_Catalog_PhoneCode
93. MLTF_MS_Catalog_PaymentMethod
94. MLTF_MS_Catalog_PaymentMethod_Detail
95. LTF_MS_Catalog_Bank
96. MLTF_MS_Catalog_BankBranch
97. MLTF_MS_Catalog_OAuth_Supplier