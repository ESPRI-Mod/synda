MODULE m_mask
CONTAINS  

   subroutine mask_sel(nystart,nyend,nycorstart,nycorend,cicaltype,sel_month,maskST,length_STT)
       USE m_ymdsju

       IMPLICIT NONE

! Ce programme crée un masque pour la fonction PACK afin d'extraire un
! sous-vecteur en fonction du mois.
!
!Arguments:
! nystart    année de début de la série temporelle
! nyend      année de fin de la série temporelle
! nycorstart année du debut de la sous-série
! nycorend   année de fin de la sous-série
! cicaltype  type de calendrier : 1=real, 2=30-day months, 3=365 days
! sel_month  mois à extraire
! maskST     vecteur du masque (output)
! length_STT Taille du sous-vecteur. (ouput)


       real, allocatable, dimension(:,:) :: TimeSerie   
       logical,INTENT(OUT),allocatable, dimension(:) :: maskST
       INTEGER,INTENT(IN) ::nystart,nyend,nycorstart,nycorend
       CHARACTER (LEN=1) :: cicaltype 
       INTEGER,INTENT(IN) :: sel_month
       INTEGER,INTENT(OUT) :: length_STT
       INTEGER, dimension(12) :: month=(/31,28,31,30,31,30,31,31,30,31,30,31/)
       INTEGER, dimension(12) :: monthbi=(/31,29,31,30,31,30,31,31,30,31,30,31/)
       INTEGER, dimension(12) :: cmonth=(/0,31,59,90,120,151,181,212,243,273,304,334/)
       INTEGER, dimension(12) :: cmonthbi=(/0,31,60,91,121,152,182,213,244,274,305,335/)
       INTEGER :: i,j,k
       INTEGER :: julian_day_deb,julian_sec,julian_day_end
       INTEGER :: lengthST,length_year
       INTEGER :: compteur_m,compteur_day,indice   
       REAL :: compteur_year
       INTEGER :: bmonth,ncmonth
       
        
       length_year=nyend - nystart + 1


        !Calcul de la taille de la série temporelle entre nystart et nyend
        ! en fonction du type de calendrier
        SELECT CASE(cicaltype)
          CASE('1')
            !standard
            CALL ymds2ju(nystart,1,01,0,cicaltype,julian_day_deb,julian_sec)
            CALL ymds2ju(nyend,12,31,0,cicaltype,julian_day_end,julian_sec)
            lengthST=julian_day_end-julian_day_deb+1
      
          CASE('2')
            !360d
            lengthST=(nyend-nystart+1)*360
       
          CASE('3')
            !365d
            lengthST=(nyend-nystart+1)*365

         END SELECT
        
        ! allocation des vecteurs
        allocate(TimeSerie(lengthST,3))
        allocate(maskST(lengthST))
     
        ! Initialisation du masque
        maskST= .FALSE.


! Creation d'un tableau couvrant la période de nystart à nyend
!       avec 3 colonnes : Year - Month - Day en fonction du calendrier

      SELECT CASE(cicaltype)
          CASE('1')
             !   calendrier réel
             compteur_day=1
             compteur_m=2
             compteur_year=nystart
             indice=0

             ! Boucle sur les années
             do i=1,length_year
                  compteur_m=1
                  
                  ! Boucle sur les mois 
                  do j=1,12
                        compteur_day=1
                        if(mod(compteur_year,4.).ne.0.or.compteur_year.eq.2100) then
                           bmonth=month(j)
                           ncmonth=cmonth(j)
                        else
                           bmonth=monthbi(j)
                           ncmonth=cmonthbi(j)
                        endif
                  
                        ! Boucle sur les jours               
                        do k=1,bmonth
                           indice=indice+1
                           TimeSerie(indice,3)=int(compteur_day)
                           TimeSerie(indice,2)=int(compteur_m)
                           TimeSerie(indice,1)=int(compteur_year)

                            compteur_day=compteur_day+1
                         enddo
                         compteur_m=compteur_m+1
                    enddo
                    compteur_year=compteur_year+1
                enddo

            
        CASE('2')
           ! Calendirer 360 days
           compteur_day=1
           compteur_m=2
           compteur_year=nystart
           
           ! Boucle sur les années
           do i=1,length_year
              compteur_m=1
  
              ! Boucle sur les mois
              do j=1,12
                 compteur_day=1
 
                 !Boucle sur les jours
                 do k=1,30
                      indice=k+(j-1)*30+(i-1)*30*12
                      TimeSerie(indice,3)=int(compteur_day)
                      TimeSerie(indice,2)=int(compteur_m)
                      TimeSerie(indice,1)=int(compteur_year)

                      compteur_day=compteur_day+1
                 enddo
                 compteur_m=compteur_m+1
              enddo
              compteur_year=compteur_year+1
          enddo
   
       CASE('3')
          ! Calendrier 365 days
          compteur_day=1
          compteur_m=2

          compteur_year=nystart

          ! Boucle sur les années
          do i=1,length_year
             compteur_m=1
             
             ! Boucle sur les mois
             do j=1,12
                 compteur_day=1
  
                 ! Boucle sur les jours
                 do k=1,month(j)
                    indice=k+cmonth(j)+(i-1)*365
                    TimeSerie(indice,3)=int(compteur_day)
                    TimeSerie(indice,2)=int(compteur_m)
                    TimeSerie(indice,1)=int(compteur_year)

                    compteur_day=compteur_day+1
                 enddo
                 compteur_m=compteur_m+1
             enddo
             compteur_year=compteur_year+1
          enddo
       END SELECT

       ! creation du masque avec des valeur TRUE pour le moi selectionné et
       ! entre les années nycorstart et nycorend
 
       maskST=TimeSerie(:,2).eq.sel_month.and.TimeSerie(:,1).ge.nycorstart.and.TimeSerie(:,1).le.nycorend

       ! Détermination de la taille du vecteur "TRUE"
       length_STT=size(PACK(TimeSerie(:,3),maskST))


END SUBROUTINE mask_sel

END MODULE m_mask



