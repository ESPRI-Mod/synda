program correction_CDFt
         
!  This program make bias correction with CDFt method.
!  This program takes a '20-year' file of climate model, a reference observation file 
!  and a reference model file and compute a '10-year' bias corrected file
!  The program works with the "worker" correction_cdft.sh
!
!
! Utilisation de :
!    la bibliothèque netcdf pour la lecture et l'écriture des fichiers netcdfs
!    la bibliotheque omp_lib pour la parallélisation openmp
!    la bibliothèque IFPORT: Portability Library
!    pour la fonction rand avec le compilateur ifort
!    
!    les modules :
!    m_cdft_pr.f90    module de correction de la pluie
!    m_cdft_tas.f90   module de correction de la temperature
!    m_mask.f90       module de création de masques
!    m_sort.f90       module de tri des données
!    m_ymdsju.f90     module de Convertion de la date en jours julien
!
! Ce programme est appelé par le "worker" correction_cdft.sh
! le worker decoupe la serie temporelle en n periodes.
! chaque période est corrigée de facon indépendante. 
!
! Ce programme est appelé avec 14 argumennts
! Name of the variable
! Initial RCM/GCM file for ref period
! Reference observation file 
! Initial RCM/GCM file for moving period
! Output BC file on obs grid
! Year of start of the file
! Year of end of the file
! Year of start of the reference period
! Year of end of the reference period
! Type of calendar; 1=real, 2=30-day months, 3=365 days
! length of moving period
! length of cor period
! number of moving period
! memory allowed in Go
!
!
!
! Date        Programmeur(s)          Historique
! ====        ==========              =====================
!             M. Vrac                 Code original en R
! 2016/01     R. Vautard              Code original en fortran
! 2016/08     T. Noel                 Adaptation et optimisation du programme
!                                     pour l'intégration dans Synda


       USE netcdf           ! Chargement librairie nectdf
       USE m_sort           ! Chargement du module de tri    
       USE m_cdft_tas       ! Chargement du module de correction de tas
       USE m_cdft_pr        ! Chargement du module de correciton de pr
       USE m_mask           ! Chargement du module de création des masques
       USE m_ymdsju         ! Chargement du module du conversion des dates en
                            ! jours julien
       USE omp_lib          ! Chargement de la librairie openmp pour la parallélisation
       USE IFPORT           ! Chargement de la librairie IFPORT pour la fonction rand

       IMPLICIT NONE


       INTEGER , PARAMETER :: ndimsmax = 4
       INTEGER , PARAMETER :: ndamax = 5000
       INTEGER :: nstep
       
       real, allocatable, dimension(:,:,:) :: datamo     ! Input data
       real, allocatable, dimension(:,:,:) :: datamoref  ! Input data for ref period

       real, allocatable, dimension(:) :: sel_datamo     ! Selection Input data
       real, allocatable, dimension(:) :: sel_datamoref  ! Selecion Ref Input data
       real, allocatable, dimension(:,:,:) :: datamoo    ! Bias corrected data
       real, allocatable, dimension(:,:,:) :: refobs     ! Observation data
       real, allocatable, dimension(:) :: sel_refobs     ! Selecion Observation data
       double precision, allocatable, dimension(:)     :: tim      ! Time variable

       real, allocatable, dimension(:) :: xfuc_mth       ! Vecteur corrigé pour un mois
       logical, allocatable, dimension(:) :: maskST,maskST_ecri    ! Masques
       logical, allocatable, dimension(:) :: maskST_ref,maskST_obs ! Masques
       INTEGER :: start_moving,end_moving,ny_cor_start,ny_cor_end  ! Années
       
       INTEGER :: length_STT,length_ST_ref,length_ST_obs ! Taille des vecteurs
       INTEGER :: length_data,length_obs,length_data_ref ! Taille des vecteurs
       INTEGER :: ram                                    ! Ram allouée au programme

       integer :: id,id_sel,id_ecri,temp_ST,ibx,iby
       real :: t1,t2,s_nb_bloc
 
       integer varid, ifileid, timid,timido,obsfileid,ifiledatad ! id netcdf
       integer dimids(ndimsmax), lendim(ndimsmax)    ! id et taille des dimensions du fichier modele
       integer dimidso(3),lendimo(ndimsmax)          ! id et taille des dimensions du fichier obs    
       integer xid,yid,oid
       character*1 icaltype                          
       integer :: intcaltype                         ! type de calendrier

       character*25 varname,varin    ! Variable
       character*50  varnamecor      !  Variable Corrigée
       character*256 namedim(ndimsmax)
       character*256 filei,fileobs,fileout,filedata
       character*256 tunit,tcal,cmoving,ccor,cperiod,cram,Ndimx,Ndimy
       
       character*256 c_nystart,c_nyend,c_nyrefstart,c_nyrefend
 
       integer :: nystart,nyend,nyrefstart,nyrefend  ! années
       integer :: nyref,nperiods
       integer :: nllast
       integer :: nx,ny,length_ST_ecri
       integer :: julian_day_deb,julian_sec,julian_day_end
       integer :: ierr,idim,nxxo,nyyo,np  
       integer :: nys,nyl
       integer :: ndims,moi
       integer :: lonid,latid,i1d
       integer :: shift,moving,cor
       integer :: length_output,deb_output,end_output      ! parametres fichier de sortie
       integer :: nx_bloc,ny_bloc,sx_bloc,sy_bloc,nb_bloc  ! blocs
       integer :: nb_blocx,nb_blocy                        ! blocs
       
       integer :: tbloc

       ! Récuperation des arguments
       CALL getarg(1,varin)         ! Name of the variable
       CALL getarg(2,filei)         ! Initial RCM/GCM file for ref period
       CALL getarg(3,fileobs)       ! Reference observation file 
       CALL getarg(4,filedata)      ! Initial RCM/GCM file for moving period
       CALL getarg(5,fileout)       ! Output BC file on obs grid
       CALL getarg(6,c_nystart)     ! Year of start of the file
       CALL getarg(7,c_nyend)       ! Year of end of the file
       CALL getarg(8,c_nyrefstart)  ! Year of start of the reference period
       CALL getarg(9,c_nyrefend)    ! Year of end of the reference period 
       CALL getarg(10,icaltype)     ! Type of calendar; 1=real, 2=30-day months, 3=365 days
       CALL getarg(11,cmoving)      ! length of moving period
       CALL getarg(12,ccor)         ! length of cor period
       CALL getarg(13,cperiod)      ! number of moving period
       CALL getarg(14,cram)         ! memory allowed in Go
       CALL getarg(15,Ndimx)        ! nom de la dimension en x
       CALL getarg(16,Ndimy)        ! nom de la dimension en y

       !Conversions des arguments dans le bon format
        varname=TRIM(varin)
        varnamecor=TRIM(varname)//"Adjust"
        READ (icaltype,'(i1)') intcaltype
        READ (c_nystart,'(i4)') nystart
        READ (c_nyend,'(i4)') nyend
        READ (c_nyrefstart,'(i4)') nyrefstart
        READ (c_nyrefend,'(i4)') nyrefend
        READ (cmoving,'(i2)') moving
        READ (ccor,'(i4)') cor
        READ (cperiod,'(i2)') np
        READ (cram,'(i2)') ram

        ! Calcul du shit entre la période de moving et la période corrigée
        shift = (moving-cor)/2

       print *,varname,varnamecor
       
       ! calcul temps préparation data - borne 1
       call cpu_time(t1)  

 
 ! Definition des paramètres en fonction de la variable à corriger

 SELECT CASE(varname)
 CASE('tas','tasmin','tasmax')
        print *,"cdft tas"
        nstep=1000   
 CASE('pr','sfcWind')
        print *,"cdft pr"
        nstep=10000
 END SELECT


      nyref = nyrefend - nyrefstart + 1 ! Length of obs period (and ref period)
      print *,"parametres :",nystart,nyend,nyrefstart,nyrefend

      ! Number of periods to correct and lenght of the last one
      ! Periods (of 20 years) are shifted by 10 years and overlap one another

       nperiods = int((nyend-nystart+1)/cor) - 1
       nllast = nyend - nystart + 1 - (nperiods-1)*cor
       print *, 'Number of correction periods:',nperiods
       print *, 'Length of the last correction period:',nllast

      !  Reading the data model ref netcdf file

       call check(nf90_open(filei, NF90_WRITE,ifileid))
       call check(nf90_inq_varid(ifileid,varname, varid))
       call check(nf90_Inquire_Variable(ifileid,varid,ndims=ndims,dimids=dimids))
       ! Boucle sur les dimensions pour récupérer les informations du fichier
       DO idim = 1,ndims
          call check(nf90_Inquire_Dimension(ifileid,dimids(idim),name = namedim(idim), len = lendim(idim)))
          print *,'RCM/GCM DIMENSION(',idim,')=',lendim(idim)
       ENDDO
       print *,'LENDIM ',lendim(ndims)
       length_data_ref=lendim(ndims)

        ! ############################################
        ! Calcul de la taille du bloc de lecture en fonction de la ram
        ! Référence :  32 Go : 720*360 : 259200 pts
        
        tbloc= ceiling((ram)*259200./32.*(nyrefend-nyrefstart+1+moving+cor)/(27+20+10))
        print *,"tbloc",tbloc
      
        ny=1
        nb_bloc=1
        ! calcul du nombre de bloc 
        do while (((lendim(1)*lendim(2))/ny)>tbloc)  
                nb_bloc= ny
                ny=ny+1  
        enddo
      
        print *,"nb_bloc",nb_bloc
        
        s_nb_bloc=sqrt(nb_bloc*1.)

        ! calcul du nombre de bloc en x et en y
        nb_blocx=ceiling(s_nb_bloc)
        nb_blocy=floor(s_nb_bloc)
  
   ! Ajustement du nombre de bloc pour eviter les dépassements mémoires
   if ((nb_blocx*nb_blocy)<nb_bloc) then
   print *,"ajustement"
   nb_blocy=nb_blocy+1
   endif
   if ((lendim(1)*lendim(2))/(nb_blocx*nb_blocy)>tbloc)then
   print *,"ajustement"
   if (nb_blocx==1)then
   nb_blocx=nb_blocx+1
   else
   nb_blocy=nb_blocy+1
   endif
   endif

   ! Taille du bloc
   print *,"taille :",(lendim(1)*lendim(2))/(nb_blocx*nb_blocy)
   ! nombre de bloc en x et en y  
   print *,"Bloc X ; Bloc Y :",nb_blocx,nb_blocy
   ! nombre de blocs total    
   print *,"n bloc :",nb_blocx*nb_blocy
   
   ! calcul de la taille des blocs
   nx_bloc=lendim(1)/nb_blocx
   ny_bloc=lendim(2)/nb_blocy
   
   print*,"bloc :",nx_bloc,ny_bloc ! Tailles de blocs  x et y


! ############################################    
! Boucle sur les blocs

do ibx=1,nb_blocx
 do iby=1,nb_blocy

       print *,"boucle sur les blocs",ibx,iby   ! numero de bloc
 
       sx_bloc=((ibx-1)*nx_bloc)+1  ! debut du bloc en x
       sy_bloc=((iby-1)*ny_bloc)+1  ! debut du bloc en y    
 
     print *,"start :",sx_bloc,sy_bloc
     print *,"count :",nx_bloc,ny_bloc
    


       ! Allocation du tableaux données model reference
       allocate(datamoref(nx_bloc,ny_bloc,length_data_ref))
       print *,'Dim datamoref :',nx_bloc,ny_bloc,length_data_ref



       !  Reading the data model netcdf file

       call check(nf90_open(filedata, NF90_WRITE,ifiledatad))
       call check(nf90_inq_varid(ifiledatad,varname, varid))
       call check(nf90_Inquire_Variable(ifiledatad,varid,ndims=ndims,dimids=dimids))
      
       ! Boucle sur les dimensions pour récupérer les informations du fichier
       DO idim = 1,ndims
          call check(nf90_Inquire_Dimension(ifiledatad,dimids(idim),name = namedim(idim), len = lendim(idim)))
          print *,'RCM/GCM DIMENSION(',idim,')=',lendim(idim)
       ENDDO
       print *,'LENDIM ',lendim(ndims)

       ! allocation du tableau des données Model
       allocate(datamo(nx_bloc,ny_bloc,lendim(ndims)))
       print *,'Dim datamo :',nx_bloc,ny_bloc,lendim(ndims)

       ! Allocation du vecteur time
       allocate(tim(lendim(ndims)))

       ! ############################################
       !  Lecture data model

       print *,ndims
       
       ! si le fichier à 4 dimensions
       if(ndims.eq.4) then
       print *,'ndim=4'
       ! recuperation variable à corriger
       call check(nf90_get_var(ifiledatad, varid,datamo,start=(/sx_bloc,sy_bloc,1,1/), &
     &        count=(/nx_bloc,ny_bloc,1,lendim(4)/)))
       endif

       ! si le fichier à 3 dimensions 
       if(ndims.eq.3) then
       print *,'ndim=3'
       ! recuperation variable à corriger
       call check(nf90_get_var(ifiledatad, varid,datamo,start=(/sx_bloc,sy_bloc,1/), &
     &        count=(/nx_bloc,ny_bloc,lendim(3)/)))
       endif


       ! Recuperation de l'id et des valeurs du temps
       call check(nf90_inq_varid(ifiledatad,'time',timid))
       call check(nf90_get_var(ifiledatad,timid,tim))

       ! Récuperation des attributs du temps : unit et calendar
       call check(nf90_get_att(ifiledatad,timid,"units",tunit))
       call check(nf90_get_att(ifiledatad,timid,"calendar",tcal))

       PRINT*,'GCM/RCM data now read'
     

       ! ############################################
       !  Lecture data reference model

       print *,ndims
       if(ndims.eq.4) then
       print *,'ndim=4'
       ! recuperation variable model reference
       call check(nf90_get_var(ifileid, varid,datamoref,start=(/sx_bloc,sy_bloc,1,1/), &
     &        count=(/nx_bloc,ny_bloc,1,length_data_ref/)))
       endif
       if(ndims.eq.3) then
       print *,'ndim=3'
       ! recuperation variable model reference
       call check(nf90_get_var(ifileid, varid,datamoref,start=(/sx_bloc,sy_bloc,1/), &
     &        count=(/nx_bloc,ny_bloc,length_data_ref/)))
       endif
       PRINT*,'data model for ref period now read'


       !############################################
       !  Reading the observation file

       call check(nf90_open(fileobs, NF90_NOWRITE,obsfileid))
       call check(nf90_inq_varid(obsfileid,varname,varid))
       call check(nf90_Inquire_Variable(obsfileid,varid,dimids=dimids))
       
       ! Boucle sur les dimensions pour récupérer les informations du fichier
       DO idim = 1,3
          call check(nf90_Inquire_Dimension(obsfileid,dimids(idim), &
    &     name = namedim(idim), len = lendimo(idim)))
          print *,'OBS DIMENSION(',idim,')=',lendimo(idim)
       ENDDO
  
       ! dimensions 
       nxxo = nx_bloc
       nyyo = ny_bloc

       !Allocation du tableau des obs
       allocate(refobs(nx_bloc,ny_bloc,lendimo(3)))
       
       length_data=lendim(ndims)
       length_obs=lendimo(3)

       ! Lecture données d'observations
       call check(nf90_get_var(obsfileid, varid,refobs,start=(/sx_bloc,sy_bloc,1/), &
     &        count=(/nx_bloc,ny_bloc,lendimo(3)/)))

       PRINT*,'All Obs data now read'

       call cpu_time(t2)  ! calcul temps préparation data - borne 2
       print* ,"time préparation data",t2-t1

       print *,'++ Preparing data'
       
       ! Boucle sur les périodes externalisée
       ! Traitement d'un période
       print *,'PERIOD=',np

       !  Start and end year of the period

          nys = (np-1)*cor + nystart
          if(np.lt.nperiods)nyl=moving
          if(np.eq.nperiods)nyl=nllast
          print *,'Starting Year:',nys
          print *,'Ending Year:',nys+nyl-1
          start_moving=nys
          end_moving=nys+nyl-1

         
        !  Calculation of period length (depends on month and calendar)
        !  Also calculation of data start

          if(np.eq.1.)ny_cor_start=start_moving
          if(np.gt.1.)ny_cor_start=start_moving+shift
          if(np.lt.nperiods)ny_cor_end=nys+shift+cor-1
          if(np.eq.nperiods)ny_cor_end=end_moving

          print *,'Start,end of output period:',ny_cor_start,ny_cor_end
          
      ! determination de la dimension du tableau de sortie en fonction du type
      ! de calendrier : length_output
      ! determination des bornes de la période corrigée : deb_output,end_output
      SELECT CASE(icaltype)
          CASE('1')
            ! Calendrier standard
            CALL ymds2ju(ny_cor_start,1,01,0,icaltype,julian_day_deb,julian_sec)
            CALL ymds2ju(ny_cor_end,12,31,0,icaltype,julian_day_end,julian_sec)

             length_output=julian_day_end-julian_day_deb+1
            
            CALL ymds2ju(start_moving,1,01,0,icaltype,julian_day_deb,julian_sec)
            CALL ymds2ju(ny_cor_start,1,01,0,icaltype,julian_day_end,julian_sec)

             deb_output=julian_day_end-julian_day_deb+1

            CALL ymds2ju(start_moving,1,01,0,icaltype,julian_day_deb,julian_sec)
            CALL ymds2ju(ny_cor_end,12,31,0,icaltype,julian_day_end,julian_sec)

             end_output=julian_day_end-julian_day_deb+1

          CASE('2')
            ! Calendrier 360 days
            CALL ymds2ju(ny_cor_start,1,01,0,icaltype,julian_day_deb,julian_sec)
            CALL ymds2ju(ny_cor_end,12,30,0,icaltype,julian_day_end,julian_sec)

            length_output=julian_day_end-julian_day_deb+1
  
            CALL ymds2ju(start_moving,1,01,0,icaltype,julian_day_deb,julian_sec)
            CALL ymds2ju(ny_cor_start,1,01,0,icaltype,julian_day_end,julian_sec)

             deb_output=julian_day_end-julian_day_deb+1

            CALL ymds2ju(start_moving,1,01,0,icaltype,julian_day_deb,julian_sec)
            CALL ymds2ju(ny_cor_end,12,30,0,icaltype,julian_day_end,julian_sec)

             end_output=julian_day_end-julian_day_deb+1
  
          CASE('3')
            ! Calendrier 365 days
            CALL ymds2ju(ny_cor_start,1,01,0,icaltype,julian_day_deb,julian_sec)
            CALL ymds2ju(ny_cor_end,12,31,0,icaltype,julian_day_end,julian_sec)

            length_output=julian_day_end-julian_day_deb+1

            CALL ymds2ju(start_moving,1,01,0,icaltype,julian_day_deb,julian_sec)
            CALL ymds2ju(ny_cor_start,1,01,0,icaltype,julian_day_end,julian_sec)

             deb_output=julian_day_end-julian_day_deb+1

            CALL ymds2ju(start_moving,1,01,0,icaltype,julian_day_deb,julian_sec)
            CALL ymds2ju(ny_cor_end,12,31,0,icaltype,julian_day_end,julian_sec)

             end_output=julian_day_end-julian_day_deb+1

         END SELECT


        print *,"L_output",length_output

        print *,"Initializing corrected data"
        ! allocation du tableau des données corrigées
        allocate(datamoo(nx_bloc,ny_bloc,length_output))

        ! Initialisation du tableau
        datamoo(:,:,:) = 1.e20

        ! Print des bornes des périodes du fichier et de la période à traiter
        print *,nystart,nyend,start_moving,end_moving
         
! Boucle sur les mois
do moi=1,12     
print *,"mois",moi
! calcul temps Boucle mois - borne 1
call cpu_time(t1)
           
    ! Masque des données Model
    CALL mask_sel(start_moving,end_moving,start_moving,end_moving,icaltype,moi,maskST,length_STT)
    ! Masque des données d'observations
    CALL mask_sel(nyrefstart,nyrefend,nyrefstart,nyrefend,'1',moi,maskST_obs,length_ST_obs)
    ! Masque des données de référence
    CALL mask_sel(nyrefstart,nyrefend,nyrefstart,nyrefend,icaltype,moi,maskST_ref,length_ST_ref)
    ! Masque d'écriture
    CALL mask_sel(start_moving,end_moving,ny_cor_start,ny_cor_end,icaltype,moi,maskST_ecri,temp_ST)


    length_ST_ecri=size(maskST_ecri(:))
    print *,"length_ST_ecri",length_ST_ecri

! début de la boucle parallele sur les points de grille
!$omp parallel default(shared) private(nx,ny,id_sel,id,xfuc_mth,sel_refobs,sel_datamoref,sel_datamo,length_ST_ecri)
!$omp do ordered schedule(dynamic)
    do ny=1,nyyo
       do nx=1,nxxo
        
       !Allocation des sous-tableaux 
        allocate(xfuc_mth(length_STT))
        allocate(sel_refobs(length_obs))
        allocate(sel_datamoref(length_data_ref))
        allocate(sel_datamo(length_data))
       
       ! initialisation des sous-tableaux
         sel_refobs=refobs(nx,ny,:)
         sel_datamo=datamo(nx,ny,:)
         sel_datamoref=datamoref(nx,ny,:)

       ! Test si données à traiter ( différent de 1e20 )
       if(refobs(nx,ny,1).lt.1.e10.and.datamo(nx,ny,1).lt.1.e10) then
       !Appel de la fonction de correction

          call correction(varname,length_data_ref,length_data,length_obs,length_ST_ref,length_ST_obs,length_STT,&
&               sel_refobs,sel_datamoref,sel_datamo,maskST_ref,maskST_obs,maskST,nstep,xfuc_mth)

!$OMP ORDERED
          ! Initialisation des indices
          id_sel=1
          id_ecri=1
          ! Boucle de parcourt du vecteur maskST_ecri
          do id=deb_output,end_output
                ! copie du vecteur données corrigées 
                ! dans le Tableau données corrigées
                if(maskST_ecri(id).eqv..TRUE.) then
                  if(xfuc_mth(id_sel).le.1e-11)then
                     ! Si la valeur est trop petite on met la valeur à 0.    
                     datamoo(nx,ny,id_ecri)=0.
                  else
                     ! Sinon on utilis la valeur corrigée
                     datamoo(nx,ny,id_ecri)=xfuc_mth(id_sel) 
                  endif
                  id_sel=id_sel+1
                endif
                id_ecri=id_ecri+1
          enddo
!$OMP END ORDERED

          endif 
          ! desallocation des vecteurs   
          deallocate(xfuc_mth)
          deallocate(sel_refobs)
          deallocate(sel_datamo)
          deallocate(sel_datamoref)

      ! Fin boucle sur les points de grilles
      enddo
    enddo 
!$omp end do
!$omp end parallel

    
 ! calcul temps Boucle mois - borne 2
 call cpu_time(t2)
 print *,"time CPU mois",t2-t1

! Fin Boucle sur les mois
end do  ! 

! calcul temps écriture des données - borne 1
call cpu_time(t1)

!  Writing bias corrected data

       print *,'Now writing output data...'

       dimidso(1)=dimids(1)
       dimidso(2)=dimids(2)
       dimidso(3)=length_output       
       print *,end_output-deb_output+1

       if (ibx.eq.1.and.iby.eq.1)then 
       ! Si premier Bloc, ouverture et definition de la variable
       ! le fichier avec les meta-données a été créé par le worker 

       ! ouverture du fichier
       call check(nf90_open(fileout, NF90_WRITE,oid))

       ! Recuperation des infos des dimensions du fichier
       !call check(nf90_Inq_Dimid(oid,'lon',dimidso(1)))
       !call check(nf90_Inq_Dimid(oid,'lat',dimidso(2)))
       call check(nf90_Inq_Dimid(oid,Ndimx,dimidso(1)))
       call check(nf90_Inq_Dimid(oid,Ndimy,dimidso(2)))

       call check(nf90_Inq_Dimid(oid,'time',dimidso(3)))

       ! Passage en mode définition
       call check(nf90_redef(oid))

       ! Definition de la variable corrigée
       call check(nf90_def_var(oid,varnamecor,NF90_REAL,dimidso,i1d))

       call check(nf90_enddef(oid))

       endif

       ! Ecriture des données  
       print *,"ecriture data" 
 
       call check(nf90_put_var(oid,i1d,datamoo,start=(/sx_bloc,sy_bloc,1/), &
     &        count=(/nx_bloc,ny_bloc,length_output/)))
      
       if (ibx.eq.nb_blocx.and.iby.eq.nb_blocy)then 
          ! si dernier bloc, cloture du fichier
          call check(nf90_close(oid))

          print *,"close data"
      endif
  
      ! calcul temps d'écriture des données - borne 2
      call cpu_time(t2)
      print *,"Time Ecriture Fichiers",t2-t1 

      !Desallocation des tableaux 
      deallocate(datamoref)
      deallocate(datamo)
      deallocate(tim)
      deallocate(refobs)

      deallocate(datamoo)

enddo ! boucle blocy
enddo ! boucle blocsx

print *,'++ BC Data on obs grid now written'

end 
      
subroutine check(status)
use netcdf
    integer, intent ( in) :: status
    ! subroutine check error netcdf
    if(status /= nf90_noerr) then 
      print *, trim(nf90_strerror(status))
      stop "Stopped"
    end if
  end subroutine check 


SUBROUTINE correction(varn,L_data_ref,L_data,L_obs,L_ST_ref,L_ST_obs,L_ST,obs_data,ref_data,mod_data,mask_data,&
& mask_obs,mask_model,snstep,sxfuc_mth)
USE m_sort
USE m_cdft_tas
USE m_cdft_pr

! subroutine de correction qui va extraire les sous-vecteur du mois à traiter 
! et appeler les modules de correction
! la subroutine extrait 3 sous vecteurs :
!  données de référence Observations pour le mois à traiter
!  données de référence Model pour le mois à traiter
!  données Model pour le mois à traiter


!Appel de la subroutine :
!correction(varname,length_data_ref,length_data,length_obs,length_ST_ref,length_ST_obs,length_STT,&
!&               sel_refobs,sel_datamoref,sel_datamo,maskST_ref,maskST_obs,maskST,nstep,xfuc_mth)


IMPLICIT NONE
integer :: s_ind(5000)
INTEGER,INTENT(IN) :: L_ST_ref,L_ST_obs,L_ST
INTEGER,INTENT(IN) :: L_data,L_obs,snstep,L_data_ref
REAL,INTENT(IN), dimension(L_obs) :: obs_data
REAL,INTENT(IN), dimension(L_data) :: mod_data
REAL,INTENT(IN), dimension(L_data_ref) :: ref_data
character (len=20),intent(in) :: varn

logical,INTENT(IN), dimension(L_obs) :: mask_obs
logical,INTENT(IN), dimension(L_data_ref) :: mask_data
logical,INTENT(IN), dimension(L_data) :: mask_model

REAL, dimension(L_ST_obs) :: xobs_mth
REAL, dimension(L_ST_ref) :: xref_mth
REAL, dimension(L_ST) :: xfut_mth
REAL,INTENT(INOUT), dimension(L_ST) :: sxfuc_mth

! intialisation des tableaux
xref_mth(:) = 1.e20
xobs_mth(:) = 1.e20
xfut_mth(:) = 1.e20

       ! extraction des sous-vecteur MOIS de référence

       xref_mth=PACK(ref_data(:),mask_data)
       xobs_mth=PACK(obs_data(:),mask_obs)
              
       ! extratction du sous-vecteur MOIS des données Model
        xfut_mth=PACK(mod_data(:),mask_model)
       

       ! Appel du module de correction en fonction de la variable à corriger
        SELECT CASE(varn)
            CASE('tas','tasmin','tasmax')
                  ! Tri des données
                  call hpsort(L_ST_ref,xref_mth,s_ind)
                  call hpsort(L_ST_obs,xobs_mth,s_ind)
                  
                   ! appel module de correction temperature
                  call cdfttas(L_ST_obs,L_ST_ref,xobs_mth,xref_mth,L_ST,xfut_mth,snstep,sxfuc_mth)

            CASE('pr','sfcWind')
                   ! Pour la précip le tri des données est fait dans 
                   ! le module après normalisation
                   ! appel module de correction précipitation
                  call cdftpr(L_ST_obs,L_ST_ref,xobs_mth,xref_mth,L_ST,xfut_mth,snstep,sxfuc_mth)

        END SELECT
        
       
END SUBROUTINE correction

 SUBROUTINE HPSORT(N,RA,IND)
! This is a fast sorting routine
! Input n: length of data; RA: to be sorted in ascending order
! Output RA: sorted, IND: index of order in input vector
      
      INTEGER,INTENT(IN) :: N
      real,INTENT(INOUT),dimension(N) :: RA
      integer,INTENT(INOUT),dimension(N) :: IND
      integer :: L,IR,RRA,I,iind,J

      L=N/2+1
      IR=N
!The index L will be decremented from its initial value during the
!"hiring" (heap creation) phase. Once it reaches 1, the index IR
!will be decremented from its initial value down to 1 during the
!"retirement-and-promotion" (heap selection) phase.
      do i=1,n
         ind(i)=i
      enddo

10    continue
      if(L > 1)then
        L=L-1
        RRA=RA(L)
        iind=ind(L)
      else
        RRA=RA(IR)
        iind=ind(IR)
        RA(IR)=RA(1)
        ind(IR)=ind(1)
        IR=IR-1
        if(IR.eq.1)then
          RA(1)=RRA
          ind(1)=iind
          return
        end if
      end if
      I=L
      J=L+L
20    if(J.le.IR)then
        if(J < IR)then
          if(RA(J) < RA(J+1))  J=J+1
        end if
        if(RRA < RA(J))then
          RA(I)=RA(J)
          ind(I)=ind(J)
          I=J; J=J+J
        else
          J=IR+1
        end if
        goto 20
      end if
      RA(I)=RRA
      ind(I)=iind
      goto 10
END subroutine HPSORT
