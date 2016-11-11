MODULE m_ymdsju
CONTAINS

SUBROUTINE ymds2ju (year,month,day,sec,tcal,julian_day,julian_sec)
!---------------------------------------------------------------------
!- Converts year, month, day and seconds into a julian day
!-
!- In 1968 in a letter to the editor of Communications of the ACM
!- (CACM, volume 11, number 10, October 1968, p.657) Henry F. Fliegel
!- and Thomas C. Van Flandern presented such an algorithm.
!-
!- See also : http://www.magnet.ch/serendipity/hermetic/cal_stud/jdn.htm
!-
!- In the case of the Gregorian calendar we have chosen to use
!- the Lilian day numbers. This is the day counter which starts
!- on the 15th October 1582.
!- This is the day at which Pope Gregory XIII introduced the
!- Gregorian calendar.
!- Compared to the true Julian calendar, which starts some
!- 7980 years ago, the Lilian days are smaler and are dealt with
!- easily on 32 bit machines. With the true Julian days you can only
!- the fraction of the day in the real part to a precision of
!- a 1/4 of a day with 32 bits.
!---------------------------------------------------------------------
  IMPLICIT NONE
  INTEGER,INTENT(IN) :: year,month,day
  INTEGER,INTENT(IN)    :: sec
  CHARACTER,INTENT(IN) :: tcal
  INTEGER,INTENT(OUT) :: julian_day
  INTEGER,INTENT(OUT)    :: julian_sec
  INTEGER :: jd,m,y,d,ml
  CHARACTER (len=20) :: calendar
  CHARACTER(LEN=20) :: calendar_used
  REAL :: one_year = 365.2425
  INTEGER :: mon_len(12)=(/31,28,31,30,31,30,31,31,30,31,30,31/)

!---------------------------------------------------------------------
  m = month
  y = year
  d = day

 calendar=tcal

! Selection du type de calendrier 
 SELECT CASE(calendar)
 CASE('gregorian','standard','proleptic_gregorian',"1")
      calendar_used = 'gregorian'
      one_year = 365.2425
      mon_len(:)=(/31,28,31,30,31,30,31,31,30,31,30,31/)
    CASE('noleap','365_day','365d',"3")
      calendar_used = 'noleap'
      one_year = 365.0
      mon_len(:)=(/31,28,31,30,31,30,31,31,30,31,30,31/)
    CASE('all_leap','366_day','366d')
      calendar_used = 'all_leap'
      one_year = 366.0
      mon_len(:)=(/31,29,31,30,31,30,31,31,30,31,30,31/)
    CASE('360_day','360d',"2")
      calendar_used = '360d'
      one_year = 360.0
      mon_len(:)=(/30,30,30,30,30,30,30,30,30,30,30,30/)
    CASE('julian')
      calendar_used = 'julian'
      one_year = 365.25
      mon_len(:)=(/31,28,31,30,31,30,31,31,30,31,30,31/)
   END SELECT
!- We deduce the calendar from the length of the year as it
!- is faster than an INDEX on the calendar variable.
  
   IF ( (one_year > 365.0).AND.(one_year < 366.0) ) THEN
!-- "Gregorian"
    jd = (1461*(y+4800+INT((m-14)/12)))/4 &
 &      +(367*(m-2-12*(INT((m-14)/12))))/12 &
 &      -(3*((y+4900+INT((m-14)/12))/100))/4 &
 &      +d-32075
    jd = jd-2299160
  ELSE IF (    (ABS(one_year-365.0) <= EPSILON(one_year))  &
 &         .OR.(ABS(one_year-366.0) <= EPSILON(one_year)) ) THEN
!-- "No leap" or "All leap"
    ml = SUM(mon_len(1:m-1))
    jd = y*NINT(one_year)+ml+(d-1)
  ELSE
!-- Calendar with regular month
    ml = NINT(one_year/12.)
    jd = y*NINT(one_year)+(m-1)*ml+(d-1)
  ENDIF
!-
  julian_day = jd
  julian_sec = sec
!------------------------------
END SUBROUTINE ymds2ju

END MODULE m_ymdsju


