
from django.urls import path
from . import views

urlpatterns = [
    path('', views.Index, name='index'),
    # path('about/', views.About, name='about'),
    # path('features/', views.Features, name='features'),
    # path('contact/', views.Contact, name='contact'),
    path('login/', views.UserLogin, name='login'),
    path('signup/', views.UserSignup, name='signup'),
    path('logout/', views.UserLogout, name='logout'),

    path('dashboard/', views.Dashboard, name='dashboard'),
    path('profile/', views.UserProfile, name='profile'),
    path('kyc/', views.KYC, name='kyc'),

    path('setting/', views.Settings, name='setting'),
    path('message/', views.Messages, name='message'),
    path('coin/', views.Coins, name='coin'),

    path('investments/', views.Investments, name='investments'),
    path('invest/<int:pk>/', views.Invest, name='invest'),
    path('history/', views.History, name='history'),
    path('asset/', views.Asset, name='asset'),
    path('fund/', views.Fund, name='fund'),
    path('payment/', views.Payment, name='payment'),
    path('deleteUserAccount/<int:pk>/', views.DeleteUserAccount, name='deleteUserAccount'),

    path('adminPage/', views.AdminPage, name='adminPage'),
    path('search/', views.Search, name='search'),
    path('viewUser/<int:pk>/', views.ViewUser, name='viewUser'),
    path('addBalance/<int:pk>/', views.AddBalance, name='addBalance'),
    path('userhistory/<int:pk>/', views.UserHistory, name='userhistory'),
    path('approvepayment/<int:pk>/', views.ApprovePayment, name='approvepayment'),
    # path('clearBalance/<int:pk>/', views.ClearBalance, name='clearBalance'),
    # path('deleteUser/<int:pk>/', views.DeleteUser, name='deleteUser'),
    # path('blockUser/<int:pk>/', views.BlockUser, name='blockUser'),

    path('newInvestment/', views.NewInvestment, name='newInvestment'),
    path('deleteInvestment/<int:pk>/', views.DeleteInvestment, name='deleteInvestment'),
    path('addPercent/<int:pk>/', views.AddPercent, name='addPercent'),

    path('newAccount/', views.NewAccount, name='newAccount'),
    path('deleteAccount/<int:pk>/', views.DeleteAccount, name='deleteAccount'),

    # path('picture/', views.UpdatePicture, name='picture'),
    # path('pin/', views.UpdatePin, name='pin'),
    # path('password/', views.UpdatePassword, name='password'),

    # path('transactionDetail/<str:pk>/', views.TransactionDetail, name='transactionDetail'),
    # path('withdraw/', views.UserWithdraw, name='withdraw'),
    # path('viewPayment/<int:account>/', views.ViewPayment, name='viewPayment'),
    # path('pay/', views.Pay, name='pay'),

    # path('loanApplication/', views.LoanApplication, name='loanApplication'),
    # path('loan/', views.UserLoan, name='loan'),
    # path('allInvestment/', views.AllInvestment, name='allInvestment'),
    # path('investment/', views.UserInvestment, name='investment'),

    # path('adminPassword/', views.AdminPassword, name='adminPassword'),
    
    # path('makeAdmin/<int:pk>/', views.MakeAdmin, name='makeAdmin')

    # path('viewUserLoan/<int:pk>/', views.ViewUserLoan, name='viewUserLoan'),
    # path('approveLoan/<int:pk>/', views.ApproveLoan, name='approveLoan'),
    # path('paidLoan/<int:pk>/', views.PaidLoan, name='paidLoan'),

    # path('viewUserInvestment/<int:pk>/', views.ViewUserInvestment, name='viewUserInvestment'),
    # path('releaseInvestment/<int:pk>/', views.ReleaseInvestment, name='releaseInvestment'),

    # path('createTransactions/<int:pk>/', views.CreateTransactions, name='createTransactions'),
    # path('deleteTransactions/<int:pk>/', views.DeleteTransactions, name='deleteTransactions'),
    # path('deleteUserTransactions/<int:pk>/', views.DeleteUserTransactions, name='deleteUserTransactions'),

    # path('newLoan/', views.NewLoan, name='newLoan'),
    # path('deleteLoan/<int:pk>/', views.DeleteLoan, name='deleteLoan'),
]
