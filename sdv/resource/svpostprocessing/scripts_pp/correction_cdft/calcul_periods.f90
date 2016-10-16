       program calcul_periods
         

       IMPLICIT NONE
       

      ! Programme qui calcul les périodes glissantes afin de découper la série
      ! temporelle à corriger en fonction des parametres de la période de
      ! lecture (moving) et de la période d'écriture (cor)
      !
      ! Arguments
      ! Année de début de la serie temporelle
      ! Année de fin de la série temporelle
      ! Taille de la période de Lecture 
      ! Taille de la période de Correction  
      ! Fichier de sortie
      !

       INTEGER :: moving,cor,shift
       

        INTEGER :: start_moving,end_moving,ny_cor_start,ny_cor_end
       
        
         character*256 c_nystart,c_nyend,c_cor,c_moving
         character*256 fileout

       integer :: nystart,nyend,nperiods
       integer :: nys,nyl,nostart,noend,k,np,nllast
       integer :: ndims,krefstart,moi,kstart,kostart,koend
       
      character*1 ::a
      a="-"

       CALL getarg(1,c_nystart)    ! Year of start of the file
       CALL getarg(2,c_nyend)      ! Ending year 
       CALL getarg(3,c_moving)     ! durée de la période de lecture (20 ans)
       CALL getarg(4,c_cor)        ! duréee de correction  (10 ans)
       CALL getarg(5,fileout)      ! fichier de sortie

        ! Conversion des paramètres en entier
        READ (c_nystart,'(i)') nystart
        READ (c_nyend,'(i)') nyend
        READ (c_moving,'(i)') moving
        READ (c_cor,'(i)') cor

        ! décalage entre période de lecture et correction
        shift = (moving-cor)/2


       print *,"parametres :",nystart,nyend

       nperiods = int((nyend-nystart+1)/cor) - 1
       nllast = nyend - nystart + 1 - (nperiods-1)*cor
       print *, 'Number of correction periods:',nperiods
       print *, 'Length of the last correction period:',nllast

! écriture sur fichier externe en latin1
 OPEN(UNIT=10, FILE=fileout, ENCODING='DEFAULT') ! latin1

       ! boucle sur les périodes
       do np=1,nperiods

          nys = (np-1)*cor + nystart
          if(np.lt.nperiods)nyl=moving
          if(np.eq.nperiods)nyl=nllast
          start_moving=nys
          end_moving=nys+nyl-1

           
          if(np.eq.1.)ny_cor_start=start_moving         !ajustement debut de la période
          if(np.gt.1.)ny_cor_start=start_moving+shift
          if(np.lt.nperiods)ny_cor_end=nys+shift+cor-1
          if(np.eq.nperiods)ny_cor_end=end_moving       !ajustement fin de la période
          
       ! écriture des paramètres de chaque période
       write(10,'(i,a,i,a,i,a,i)'),start_moving,"-",end_moving,"-",ny_cor_start,"-",ny_cor_end

         enddo

        CLOSE(10)

     end 

