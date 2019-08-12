daily_robot_report="""SELECT
		a.date,
		ROUND(a.`日活跃用户数`,0) as 'dau',
		ROUND(a.`新访问用户数`,0) as 'new_lauch',
		ROUND(b.`新注册用户数`,0) as 'new_member_cnt',
		z.total_member,
		ROUND(100*b.`新注册用户数`/a.`新访问用户数`,4) as 'enrollment_rate' ,
		c.`认证用户数` as 'new_certify_cnt' ,
		zz.`累计认证用户数` as 'total_crew',
		ROUND(100*c.`认证用户数`/b.`新注册用户数`,4) as 'certified_rate',
		d.`订单人数` as 'order_person_cnt',
		d.`订单数` as 'order_cnt',
		d.`当日订单转化人数` as 'today_pay_cnt',
		
		round(100*d.`当日订单转化人数`/b.`新注册用户数`,4) as 'today_pay_rate',
	
		d.`培训订单数` as 'train_cnt',
		d.`办证订单数` as 'certified_cnt',
		d.`体检订单数` as 'exam_cnt',
		ROUND(d.`流水`,0) as 'order_amt',
		d.`培训流水` as 'train_amt',
		d.`办证流水` as 'certified_amt',
		d.`体检流水` as 'exam_amt',
		ROUND(d.`流水`/d.`订单数`,0) as 'arpu',
		n.add_new AS 'new_fans',
		n.sub_new AS 'cancel_fans',
		m.cumulate_user AS 'total_fans',
		x.`合伙人活跃人数` as 'partner_use' ,
		b.`合伙人拉新注册人数` as 'partner_new_member_cnt',
		y.`合伙人拉新认证数` as 'partner_new_certify_cnt',
		round(100*y.`合伙人拉新认证数`/b.`合伙人拉新注册人数`,4) as 'partner_certified_rate'
	FROM

	-- 友盟数据
	(select date,sum(new_users) as '新访问用户数',sum(active_users) as '日活跃用户数' from umneg_appdata where date>='2019-07-01'
	group by 1) a 

	left join 

	(-- 注册用户数
	select substring(created_at,1,10)  as 'date', count(phone) as '新注册用户数', count(if(channel='membertree',true,null)) as '合伙人拉新注册人数' from member where created_at>'2019-07-01 00:00:00'

	group by 1) b  on a.date=b.date


	left join 
	(-- 认证用户数
	select substring(created_at,1,10)  as 'date',count(member_id) as '认证用户数' from member_cv 
	where created_at>'2019-07-01 00:00:00'
	and crew_type in (1,2,4)
	group by 1)  c on a.date=c.date

	left join 

	(-- 付费用户数
	SELECT
		substring(created_at, 1, 10 ) AS 'date',
		
		count(distinct phone) as '订单人数',
		count(distinct if(target=1,true,null)) as '当日订单转化人数',
		
		count(order_number) as '订单数',
		sum(real_money) as '流水',
		
		count(if(type=1,true,null)) as '培训订单数',
		sum(if(type=1,real_money,0)) as '培训流水',
		
		count(if(type=2,true,null)) as '办证订单数',
		sum(if(type=2,real_money,0)) as '办证流水',
		
		count(if(type=4,true,null)) as '体检订单数',
		sum(if(type=4,real_money,0)) as '体检流水'
	FROM
		(select a.*,if(b.created_at>=date_sub(curdate(),interval 1 day),1,0) as target from 
(select * from `order`
where created_at > '2019-07-01 00:00:00' AND real_pay_status = 2 ) a	
left join member b on a.member_id=b.id) temp
	WHERE
		temp.created_at > '2019-07-01 00:00:00' 
		AND temp.real_pay_status = 2 
	GROUP BY
		1


	) d on d.date=a.date
		
		
	left join 
		(select ref_date,cumulate_user from log_wechat_usercumulate order by 1) m on m.ref_date=a.date
	left join 
	(select ref_date,sum(new_user) as add_new,sum(cancel_user) as sub_new from log_wechat_usersummary 
	group by 1
	order by ref_date) n on m.ref_date=n.ref_date

	left join (select substring(created_at,1,10)  as 'date',count(distinct level_father_id) as '合伙人活跃人数' from member_tree where created_at>'2019-07-01 00:00:00' group by 1
	) x on x.date=a.date


	left join 

	(select substring(a.created_at,1,10) as 'date',count(if(b.level_father_id<>0,true,null)) as '合伙人拉新认证数' from 
	(select created_at,member_id from member_cv where created_at>'2019-07-01 00:00:00') a 
	left join member_tree b on a.member_id=b.member_id
	group by 1) y on y.date=a.date

	left join 
	(select date_sub(curdate(),interval 1 day) as 'date',count(*) as total_member from member) z on z.date=a.date

	left join 
	(select date_sub(curdate(),interval 1 day) as 'date',count(member_id) as '累计认证用户数' from member_cv 
	where crew_type in (1,2,4)) zz on zz.date=a.date

	where a.date=date_sub(curdate(),interval 1 day)
	"""




daily_kf_report='''select wechat_name,date_day,total,increase_num,add_adopt_num,added_num,reduce_num,chat_num from s_wx_cs
where wechat_name like '%%航运%%' and date_day=date_sub(curdate(),interval 1 day)'''

sql_order="""select id,	old_id,	type,	order_number,	log_id,	member_id,	phone	,money,	real_money,	pay_driver,	pay_gateway,pay_status,	pay_order,	pay_time,	coupon_ids,	do_status,	is_del	,body	,real_pay_status,progress,	info,	is_process,	created_at,	updated_at,	ext
from `order` where created_at between date_sub(curdate(),interval 1 day) and curdate() """

sql_member="""select id,phone,phone_city,phone_province,password,type,do_status,	audit_status,reason	,email,	recommend_phone,device_id,source,channel,userid,	uid,	surplus_money,star,vip,last_login_time,	wechat_cs_id,check_confirmation,created_at,	updated_at 
from `member` where created_at between date_sub(curdate(),interval 1 day) and curdate() """

sql_member_tree="""select id	,member_id,	level_grandpa_id,	level_father_id,	do_status	,money,	cold_money,	history_money,	bank_name,	bank_sub_name,	card_number,	payee,	version,	cv_check,	payment_check,	login_num	,black_card,	created_at,	updated_at
from `member_tree` where created_at between date_sub(curdate(),interval 1 day) and curdate() """

sql_member_cv="""select 
id,	member_id,	avatar	,user_name,	real_name,	card_id,	weixin_name,	sign_info,	gender,	birth_date,	current_position,	certificate_level,	cert_ship_route,	cert_level,	cert_position,	english_level,	work_life	,ship_type,	graduate_school,	education,	prov_id,	city_id,	contact_phone,	emergency_contact_person,	emergency_contact_number,	native_place,	do_status,	show_num,	crew_type,	blood_type	,shoe_size,	height	,weight,created_at,	updated_at,	showdated_at
from `member_cv` where created_at between date_sub(curdate(),interval 1 day) and curdate() """

sql_vip_summary="""SELECT
	a.d,
	a.company_login_cnt,
	ifnull( b.vip_pay_cnt, 0 ) AS 'vip_pay_cnt',
	ifnull( c.job_publish_company_cnt, 0 ) AS 'job_publish_company_cnt',
	ifnull(c.job_cnt,0) as 'job_cnt',
	ifnull(c.vip_job_cnt,0) as 'vip_job_cnt',
	ifnull(c.vip_company_cnt,0) as 'vip_company_cnt',
	d.crew_2_company_distinct_cnt,
	d.company_2_crew_cnt,
	d.vipCompany_2_crew_distinct_cnt,
	d.vipCompany_2_crew_cnt 
FROM

(-- 企业账号登录数
select substring(last_login_time,1,10) as d,count(id) as 'company_login_cnt' from member where type=2
and created_at>='2019-08-01 00:00:00'
group by 1) a left join 


(-- 领取vip特权数量
select substring(date_sub(vip_endtime,interval 30 day),1,10) as d,count(member_id) as 'vip_pay_cnt' from member_company_info where vip_level=1 and created_at>='2019-08-01 00:00:00' group by 1) b on a.d=b.d


left join 
(-- 所有企业数,发布职位数,vip企业数,vip企业发布职位数据
select substring(created_at,1,10) as d,count(distinct a.uid) as 'job_publish_company_cnt',count(a.id) as 'job_cnt',count(if(b.vip_level=1,1,null)) as 'vip_job_cnt',
count(distinct (case when b.vip_level=1 then a.uid end) ) as 'vip_company_cnt'
from job_publish a 
left join (select member_id,vip_level,company_name from member_company_info where vip_level=1) b on a.uid=b.member_id
where a.created_at>='2019-08-01 00:00:00'
group by 1) c on c.d=a.d

left join 


(--  每天有多少认证船员联系企业，每天认证船员联系企业的总次数,每天多少VIP企业联系了船员，每天VIP企业联系船员的总次数
select  
substring(created_at,1,10) as d,
count(distinct (case when l.jobpublish_id is not null then l.uid end)) as 'crew_2_company_distinct_cnt',  -- 船员联系企业 船员数量
count((case when l.jobpublish_id is not null then l.uid end)) as 'company_2_crew_cnt',-- 船员联系企业的次数 

count(distinct (case when l.cv_id is not null and c.vip_level=1 then l.company_id end)) as 'vipCompany_2_crew_distinct_cnt',   -- vip企业联系船员 vip企业数
count((case when l.cv_id is not null and c.vip_level=1 then l.company_id end)) as 'vipCompany_2_crew_cnt'   -- vip企业联系船员的总次数
from job_showphone_log l left join 
(select member_id,vip_level,company_name from member_company_info where vip_level=1 and company_name<>'航运e家') c on c.member_id=l.company_id
where l.created_at>='2019-08-01 00:00:00'
group by 1) d on d.d=a.d
where a.d=date_sub(curdate(),interval 1 day)

"""


daily_vip_sumary="""select * from stage_vip_summary where d=date_sub(curdate(),interval 1 day)
"""




daily_kf_wechatlist='''SELECT
	phone,
	created_at,
IF(wechat_cs_id = 1,'珊珊--李灵珊',
IF(wechat_cs_id = 2,'小朱',
IF(wechat_cs_id = 3,'小凡--郭雨琛',
IF(wechat_cs_id = 4,'晶晶姐--汪晶',
IF(wechat_cs_id = 5,'王茜子',
IF(wechat_cs_id = 6,'袁小娟',
IF(wechat_cs_id = 7, '欣欣--鲁尔妮', 
IF(wechat_cs_id = 8, '吴老轨--吴承浩', 
IF(wechat_cs_id = 9, '依琳--彭春春', '未分配' ) ) ) ) ) ) ) ) ) as 'kf'
FROM
	member 
WHERE
	created_at >= date_sub(curdate(),interval 1 day) and created_at<= curdate()
AND phone NOT IN ( SELECT mobile FROM block_list )
'''


# where created_at between date_sub(curdate(),interval 1 day) and curdate()
# where created_at <'2019-08-05 00:00:00'




