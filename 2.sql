INSERT INTO courses(date, weekday, title, course_type, start_time, end_time, is_rest, is_self_study)
VALUES('2026-06-16',
       CASE strftime('%w', '2026-06-16')
           WHEN '0' THEN '星期日'
           WHEN '1' THEN '星期一'
           WHEN '2' THEN '星期二'
           WHEN '3' THEN '星期三'
           WHEN '4' THEN '星期四'
           WHEN '5' THEN '星期五'
           WHEN '6' THEN '星期六'
       END,
       '大模型开发入门V6.0', 'lecture', '19:25', '22:30', NULL, 0),
      ('2026-06-17',
       CASE strftime('%w', '2026-06-17')
           WHEN '0' THEN '星期日'
           WHEN '1' THEN '星期一'
           WHEN '2' THEN '星期二'
           WHEN '3' THEN '星期三'
           WHEN '4' THEN '星期四'
           WHEN '5' THEN '星期五'
           WHEN '6' THEN '星期六'
       END,
       '大模型开发入门V6.0', 'lecture', '19:25', '22:30', NULL, 0),
      ('2026-06-20',
       CASE strftime('%w', '2026-06-20')
           WHEN '0' THEN '星期日'
           WHEN '1' THEN '星期一'
           WHEN '2' THEN '星期二'
           WHEN '3' THEN '星期三'
           WHEN '4' THEN '星期四'
           WHEN '5' THEN '星期五'
           WHEN '6' THEN '星期六'
       END,
       '大模型开发入门V6.0', 'lecture', '19:25', '22:30', NULL, 0),
      ('2026-06-21',
       CASE strftime('%w', '2026-06-21')
           WHEN '0' THEN '星期日'
           WHEN '1' THEN '星期一'
           WHEN '2' THEN '星期二'
           WHEN '3' THEN '星期三'
           WHEN '4' THEN '星期四'
           WHEN '5' THEN '星期五'
           WHEN '6' THEN '星期六'
       END,
       '大模型开发入门V6.0', 'lecture', '19:25', '22:30', NULL, 0),
      ('2026-06-22',
       CASE strftime('%w', '2026-06-22')
           WHEN '0' THEN '星期日'
           WHEN '1' THEN '星期一'
           WHEN '2' THEN '星期二'
           WHEN '3' THEN '星期三'
           WHEN '4' THEN '星期四'
           WHEN '5' THEN '星期五'
           WHEN '6' THEN '星期六'
       END,
       '自习', 'self_study', '10:00', '12:00', 0, 1),
      ('2026-06-22',
       CASE strftime('%w', '2026-06-22')
           WHEN '0' THEN '星期日'
           WHEN '1' THEN '星期一'
           WHEN '2' THEN '星期二'
           WHEN '3' THEN '星期三'
           WHEN '4' THEN '星期四'
           WHEN '5' THEN '星期五'
           WHEN '6' THEN '星期六'
       END,
       '自习', 'self_study', '14:00', '17:00', 0, 1),
      ('2026-06-23',
       CASE strftime('%w', '2026-06-23')
           WHEN '0' THEN '星期日'
           WHEN '1' THEN '星期一'
           WHEN '2' THEN '星期二'
           WHEN '3' THEN '星期三'
           WHEN '4' THEN '星期四'
           WHEN '5' THEN '星期五'
           WHEN '6' THEN '星期六'
       END,
       '大模型开发入门V6.0', 'lecture', '08:30', '12:20', 0, 0),
      ('2026-06-23',
       CASE strftime('%w', '2026-06-23')
           WHEN '0' THEN '星期日'
           WHEN '1' THEN '星期一'
           WHEN '2' THEN '星期二'
           WHEN '3' THEN '星期三'
           WHEN '4' THEN '星期四'
           WHEN '5' THEN '星期五'
           WHEN '6' THEN '星期六'
       END,
       '大模型开发入门V6.0', 'lecture', '14:30', '18:20', 0, 0),
      ('2026-06-23',
       CASE strftime('%w', '2026-06-23')
           WHEN '0' THEN '星期日'
           WHEN '1' THEN '星期一'
           WHEN '2' THEN '星期二'
           WHEN '3' THEN '星期三'
           WHEN '4' THEN '星期四'
           WHEN '5' THEN '星期五'
           WHEN '6' THEN '星期六'
       END,
       '大模型开发入门V6.0', 'lecture', '19:25', '22:30', NULL, 0),
      ('2026-06-24',
       CASE strftime('%w', '2026-06-24')
           WHEN '0' THEN '星期日'
           WHEN '1' THEN '星期一'
           WHEN '2' THEN '星期二'
           WHEN '3' THEN '星期三'
           WHEN '4' THEN '星期四'
           WHEN '5' THEN '星期五'
           WHEN '6' THEN '星期六'
       END,
       '大模型开发入门V6.0', 'lecture', '08:30', '12:20', 0, 0),
      ('2026-06-24',
       CASE strftime('%w', '2026-06-24')
           WHEN '0' THEN '星期日'
           WHEN '1' THEN '星期一'
           WHEN '2' THEN '星期二'
           WHEN '3' THEN '星期三'
           WHEN '4' THEN '星期四'
           WHEN '5' THEN '星期五'
           WHEN '6' THEN '星期六'
       END,
       '大模型开发入门V6.0', 'lecture', '14:30', '18:20', 0, 0),
      ('2026-06-24',
       CASE strftime('%w', '2026-06-24')
           WHEN '0' THEN '星期日'
           WHEN '1' THEN '星期一'
           WHEN '2' THEN '星期二'
           WHEN '3' THEN '星期三'
           WHEN '4' THEN '星期四'
           WHEN '5' THEN '星期五'
           WHEN '6' THEN '星期六'
       END,
       '大模型开发入门V6.0', 'lecture', '19:25', '22:30', NULL, 0),
      ('2026-06-25',
       CASE strftime('%w', '2026-06-25')
           WHEN '0' THEN '星期日'
           WHEN '1' THEN '星期一'
           WHEN '2' THEN '星期二'
           WHEN '3' THEN '星期三'
           WHEN '4' THEN '星期四'
           WHEN '5' THEN '星期五'
           WHEN '6' THEN '星期六'
       END,
       '休息', 'rest', NULL, NULL, 1, 0),
      ('2026-06-26',
       CASE strftime('%w', '2026-06-26')
           WHEN '0' THEN '星期日'
           WHEN '1' THEN '星期一'
           WHEN '2' THEN '星期二'
           WHEN '3' THEN '星期三'
           WHEN '4' THEN '星期四'
           WHEN '5' THEN '星期五'
           WHEN '6' THEN '星期六'
       END,
       '大模型开发入门V6.0', 'lecture', '08:30', '12:20', 0, 0),
      ('2026-06-26',
       CASE strftime('%w', '2026-06-26')
           WHEN '0' THEN '星期日'
           WHEN '1' THEN '星期一'
           WHEN '2' THEN '星期二'
           WHEN '3' THEN '星期三'
           WHEN '4' THEN '星期四'
           WHEN '5' THEN '星期五'
           WHEN '6' THEN '星期六'
       END,
       '大模型开发入门V6.0', 'lecture', '14:30', '18:20', 0, 0),
      ('2026-06-26',
       CASE strftime('%w', '2026-06-26')
           WHEN '0' THEN '星期日'
           WHEN '1' THEN '星期一'
           WHEN '2' THEN '星期二'
           WHEN '3' THEN '星期三'
           WHEN '4' THEN '星期四'
           WHEN '5' THEN '星期五'
           WHEN '6' THEN '星期六'
       END,
       '大模型开发入门V6.0', 'lecture', '19:25', '22:30', NULL, 0),
      ('2026-06-27',
       CASE strftime('%w', '2026-06-27')
           WHEN '0' THEN '星期日'
           WHEN '1' THEN '星期一'
           WHEN '2' THEN '星期二'
           WHEN '3' THEN '星期三'
           WHEN '4' THEN '星期四'
           WHEN '5' THEN '星期五'
           WHEN '6' THEN '星期六'
       END,
       '大模型开发入门V6.0', 'lecture', '08:30', '12:20', 0, 0),
      ('2026-06-27',
       CASE strftime('%w', '2026-06-27')
           WHEN '0' THEN '星期日'
           WHEN '1' THEN '星期一'
           WHEN '2' THEN '星期二'
           WHEN '3' THEN '星期三'
           WHEN '4' THEN '星期四'
           WHEN '5' THEN '星期五'
           WHEN '6' THEN '星期六'
       END,
       '大模型开发入门V6.0', 'lecture', '14:30', '18:20', 0, 0),
      ('2026-06-27',
       CASE strftime('%w', '2026-06-27')
           WHEN '0' THEN '星期日'
           WHEN '1' THEN '星期一'
           WHEN '2' THEN '星期二'
           WHEN '3' THEN '星期三'
           WHEN '4' THEN '星期四'
           WHEN '5' THEN '星期五'
           WHEN '6' THEN '星期六'
       END,
       '大模型开发入门V6.0', 'lecture', '19:25', '22:30', NULL, 0),
      ('2026-06-28',
       CASE strftime('%w', '2026-06-28')
           WHEN '0' THEN '星期日'
           WHEN '1' THEN '星期一'
           WHEN '2' THEN '星期二'
           WHEN '3' THEN '星期三'
           WHEN '4' THEN '星期四'
           WHEN '5' THEN '星期五'
           WHEN '6' THEN '星期六'
       END,
       '自习', 'self_study', '10:00', '12:00', 0, 1),
      ('2026-06-28',
       CASE strftime('%w', '2026-06-28')
           WHEN '0' THEN '星期日'
           WHEN '1' THEN '星期一'
           WHEN '2' THEN '星期二'
           WHEN '3' THEN '星期三'
           WHEN '4' THEN '星期四'
           WHEN '5' THEN '星期五'
           WHEN '6' THEN '星期六'
       END,
       '自习', 'self_study', '14:00', '17:00', 0, 1),
      ('2026-06-28',
       CASE strftime('%w', '2026-06-28')
           WHEN '0' THEN '星期日'
           WHEN '1' THEN '星期一'
           WHEN '2' THEN '星期二'
           WHEN '3' THEN '星期三'
           WHEN '4' THEN '星期四'
           WHEN '5' THEN '星期五'
           WHEN '6' THEN '星期六'
       END,
       '大模型语言进阶V4.0', 'lecture', '08:30', '12:20', 0, 0),
      ('2026-06-28',
       CASE strftime('%w', '2026-06-28')
           WHEN '0' THEN '星期日'
           WHEN '1' THEN '星期一'
           WHEN '2' THEN '星期二'
           WHEN '3' THEN '星期三'
           WHEN '4' THEN '星期四'
           WHEN '5' THEN '星期五'
           WHEN '6' THEN '星期六'
       END,
       '大模型语言进阶V4.0', 'lecture', '14:30', '18:20', 0, 0),
      ('2026-06-28',
       CASE strftime('%w', '2026-06-28')
           WHEN '0' THEN '星期日'
           WHEN '1' THEN '星期一'
           WHEN '2' THEN '星期二'
           WHEN '3' THEN '星期三'
           WHEN '4' THEN '星期四'
           WHEN '5' THEN '星期五'
           WHEN '6' THEN '星期六'
       END,
       '大模型语言进阶V4.0', 'lecture', '19:25', '22:30', NULL, 0),
      ('2026-06-29',
       CASE strftime('%w', '2026-06-29')
           WHEN '0' THEN '星期日'
           WHEN '1' THEN '星期一'
           WHEN '2' THEN '星期二'
           WHEN '3' THEN '星期三'
           WHEN '4' THEN '星期四'
           WHEN '5' THEN '星期五'
           WHEN '6' THEN '星期六'
       END,
       '大模型语言进阶V4.0', 'lecture', '08:30', '12:20', 0, 0),
      ('2026-06-29',
       CASE strftime('%w', '2026-06-29')
           WHEN '0' THEN '星期日'
           WHEN '1' THEN '星期一'
           WHEN '2' THEN '星期二'
           WHEN '3' THEN '星期三'
           WHEN '4' THEN '星期四'
           WHEN '5' THEN '星期五'
           WHEN '6' THEN '星期六'
       END,
       '大模型语言进阶V4.0', 'lecture', '14:30', '18:20', 0, 0),
      ('2026-06-29',
       CASE strftime('%w', '2026-06-29')
           WHEN '0' THEN '星期日'
           WHEN '1' THEN '星期一'
           WHEN '2' THEN '星期二'
           WHEN '3' THEN '星期三'
           WHEN '4' THEN '星期四'
           WHEN '5' THEN '星期五'
           WHEN '6' THEN '星期六'
       END,
       '大模型语言进阶V4.0', 'lecture', '19:25', '22:30', NULL, 0),
      ('2026-06-30',
       CASE strftime('%w', '2026-06-30')
           WHEN '0' THEN '星期日'
           WHEN '1' THEN '星期一'
           WHEN '2' THEN '星期二'
           WHEN '3' THEN '星期三'
           WHEN '4' THEN '星期四'
           WHEN '5' THEN '星期五'
           WHEN '6' THEN '星期六'
       END,
       '大模型语言进阶V4.0', 'lecture', '08:30', '12:20', 0, 0),
      ('2026-06-30',
       CASE strftime('%w', '2026-06-30')
           WHEN '0' THEN '星期日'
           WHEN '1' THEN '星期一'
           WHEN '2' THEN '星期二'
           WHEN '3' THEN '星期三'
           WHEN '4' THEN '星期四'
           WHEN '5' THEN '星期五'
           WHEN '6' THEN '星期六'
       END,
       '大模型语言进阶V4.0', 'lecture', '14:30', '18:20', 0, 0),
      ('2026-06-30',
       CASE strftime('%w', '2026-06-30')
           WHEN '0' THEN '星期日'
           WHEN '1' THEN '星期一'
           WHEN '2' THEN '星期二'
           WHEN '3' THEN '星期三'
           WHEN '4' THEN '星期四'
           WHEN '5' THEN '星期五'
           WHEN '6' THEN '星期六'
       END,
       '大模型语言进阶V4.0', 'lecture', '19:25', '22:30', NULL, 0),
      ('2026-07-01',
       CASE strftime('%w', '2026-07-01')
           WHEN '0' THEN '星期日'
           WHEN '1' THEN '星期一'
           WHEN '2' THEN '星期二'
           WHEN '3' THEN '星期三'
           WHEN '4' THEN '星期四'
           WHEN '5' THEN '星期五'
           WHEN '6' THEN '星期六'
       END,
       '休息', 'rest', NULL, NULL, 1, 0),
      ('2026-07-01',
       CASE strftime('%w', '2026-07-01')
           WHEN '0' THEN '星期日'
           WHEN '1' THEN '星期一'
           WHEN '2' THEN '星期二'
           WHEN '3' THEN '星期三'
           WHEN '4' THEN '星期四'
           WHEN '5' THEN '星期五'
           WHEN '6' THEN '星期六'
       END,
       '大模型开发入门V6.0', 'lecture', '08:30', '12:20', 0, 0),
      ('2026-07-01',
       CASE strftime('%w', '2026-07-01')
           WHEN '0' THEN '星期日'
           WHEN '1' THEN '星期一'
           WHEN '2' THEN '星期二'
           WHEN '3' THEN '星期三'
           WHEN '4' THEN '星期四'
           WHEN '5' THEN '星期五'
           WHEN '6' THEN '星期六'
       END,
       '大模型开发入门V6.0', 'lecture', '14:30', '18:20', 0, 0),
      ('2026-07-01',
       CASE strftime('%w', '2026-07-01')
           WHEN '0' THEN '星期日'
           WHEN '1' THEN '星期一'
           WHEN '2' THEN '星期二'
           WHEN '3' THEN '星期三'
           WHEN '4' THEN '星期四'
           WHEN '5' THEN '星期五'
           WHEN '6' THEN '星期六'
       END,
       '大模型开发入门V6.0', 'lecture', '19:25', '22:30', NULL, 0),
      ('2026-07-02',
       CASE strftime('%w', '2026-07-02')
           WHEN '0' THEN '星期日'
           WHEN '1' THEN '星期一'
           WHEN '2' THEN '星期二'
           WHEN '3' THEN '星期三'
           WHEN '4' THEN '星期四'
           WHEN '5' THEN '星期五'
           WHEN '6' THEN '星期六'
       END,
       '大模型开发入门V6.0', 'lecture', '08:30', '12:20', 0, 0),
      ('2026-07-02',
       CASE strftime('%w', '2026-07-02')
           WHEN '0' THEN '星期日'
           WHEN '1' THEN '星期一'
           WHEN '2' THEN '星期二'
           WHEN '3' THEN '星期三'
           WHEN '4' THEN '星期四'
           WHEN '5' THEN '星期五'
           WHEN '6' THEN '星期六'
       END,
       '大模型开发入门V6.0', 'lecture', '14:30', '18:20', 0, 0),
      ('2026-07-02',
       CASE strftime('%w', '2026-07-02')
           WHEN '0' THEN '星期日'
           WHEN '1' THEN '星期一'
           WHEN '2' THEN '星期二'
           WHEN '3' THEN '星期三'
           WHEN '4' THEN '星期四'
           WHEN '5' THEN '星期五'
           WHEN '6' THEN '星期六'
       END,
       '大模型开发入门V6.0', 'lecture', '19:25', '22:30', NULL, 0),
      ('2026-07-03',
       CASE strftime('%w', '2026-07-03')
           WHEN '0' THEN '星期日'
           WHEN '1' THEN '星期一'
           WHEN '2' THEN '星期二'
           WHEN '3' THEN '星期三'
           WHEN '4' THEN '星期四'
           WHEN '5' THEN '星期五'
           WHEN '6' THEN '星期六'
       END,
       '大模型开发入门V6.0', 'lecture', '08:30', '12:20', 0, 0),
      ('2026-07-03',
       CASE strftime('%w', '2026-07-03')
           WHEN '0' THEN '星期日'
           WHEN '1' THEN '星期一'
           WHEN '2' THEN '星期二'
           WHEN '3' THEN '星期三'
           WHEN '4' THEN '星期四'
           WHEN '5' THEN '星期五'
           WHEN '6' THEN '星期六'
       END,
       '大模型开发入门V6.0', 'lecture', '14:30', '18:20', 0, 0),
      ('2026-07-03',
       CASE strftime('%w', '2026-07-03')
           WHEN '0' THEN '星期日'
           WHEN '1' THEN '星期一'
           WHEN '2' THEN '星期二'
           WHEN '3' THEN '星期三'
           WHEN '4' THEN '星期四'
           WHEN '5' THEN '星期五'
           WHEN '6' THEN '星期六'
       END,
       '大模型开发入门V6.0', 'lecture', '19:25', '22:30', NULL, 0),
      ('2026-07-04',
       CASE strftime('%w', '2026-07-04')
           WHEN '0' THEN '星期日'
           WHEN '1' THEN '星期一'
           WHEN '2' THEN '星期二'
           WHEN '3' THEN '星期三'
           WHEN '4' THEN '星期四'
           WHEN '5' THEN '星期五'
           WHEN '6' THEN '星期六'
       END,
       '自习', 'self_study', '10:00', '12:00', 0, 1),
      ('2026-07-04',
       CASE strftime('%w', '2026-07-04')
           WHEN '0' THEN '星期日'
           WHEN '1' THEN '星期一'
           WHEN '2' THEN '星期二'
           WHEN '3' THEN '星期三'
           WHEN '4' THEN '星期四'
           WHEN '5' THEN '星期五'
           WHEN '6' THEN '星期六'
       END,
       '自习', 'self_study', '14:00', '17:00', 0, 1),
      ('2026-07-05',
       CASE strftime('%w', '2026-07-05')
           WHEN '0' THEN '星期日'
           WHEN '1' THEN '星期一'
           WHEN '2' THEN '星期二'
           WHEN '3' THEN '星期三'
           WHEN '4' THEN '星期四'
           WHEN '5' THEN '星期五'
           WHEN '6' THEN '星期六'
       END,
       '休息', 'rest', NULL, NULL, 1, 0),
      ('2026-07-05',
       CASE strftime('%w', '2026-07-05')
           WHEN '0' THEN '星期日'
           WHEN '1' THEN '星期一'
           WHEN '2' THEN '星期二'
           WHEN '3' THEN '星期三'
           WHEN '4' THEN '星期四'
           WHEN '5' THEN '星期五'
           WHEN '6' THEN '星期六'
       END,
       '大模型语言进阶V4.0', 'lecture', '08:30', '12:20', 0, 0),
      ('2026-07-05',
       CASE strftime('%w', '2026-07-05')
           WHEN '0' THEN '星期日'
           WHEN '1' THEN '星期一'
           WHEN '2' THEN '星期二'
           WHEN '3' THEN '星期三'
           WHEN '4' THEN '星期四'
           WHEN '5' THEN '星期五'
           WHEN '6' THEN '星期六'
       END,
       '大模型语言进阶V4.0', 'lecture', '14:30', '18:20', 0, 0),
      ('2026-07-05',
       CASE strftime('%w', '2026-07-05')
           WHEN '0' THEN '星期日'
           WHEN '1' THEN '星期一'
           WHEN '2' THEN '星期二'
           WHEN '3' THEN '星期三'
           WHEN '4' THEN '星期四'
           WHEN '5' THEN '星期五'
           WHEN '6' THEN '星期六'
       END,
       '大模型语言进阶V4.0', 'lecture', '19:25', '22:30', NULL, 0),
      ('2026-07-06',
       CASE strftime('%w', '2026-07-06')
           WHEN '0' THEN '星期日'
           WHEN '1' THEN '星期一'
           WHEN '2' THEN '星期二'
           WHEN '3' THEN '星期三'
           WHEN '4' THEN '星期四'
           WHEN '5' THEN '星期五'
           WHEN '6' THEN '星期六'
       END,
       '大模型语言进阶V4.0', 'lecture', '08:30', '12:20', 0, 0),
      ('2026-07-06',
       CASE strftime('%w', '2026-07-06')
           WHEN '0' THEN '星期日'
           WHEN '1' THEN '星期一'
           WHEN '2' THEN '星期二'
           WHEN '3' THEN '星期三'
           WHEN '4' THEN '星期四'
           WHEN '5' THEN '星期五'
           WHEN '6' THEN '星期六'
       END,
       '大模型语言进阶V4.0', 'lecture', '14:30', '18:20', 0, 0),
      ('2026-07-06',
       CASE strftime('%w', '2026-07-06')
           WHEN '0' THEN '星期日'
           WHEN '1' THEN '星期一'
           WHEN '2' THEN '星期二'
           WHEN '3' THEN '星期三'
           WHEN '4' THEN '星期四'
           WHEN '5' THEN '星期五'
           WHEN '6' THEN '星期六'
       END,
       '大模型语言进阶V4.0', 'lecture', '19:25', '22:00', NULL, 0);