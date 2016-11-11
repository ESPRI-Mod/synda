PROGRAM standardization

  !
  ! Filtre permettant de transformer les fichiers de serie temporelle a une 
  ! variable de l'IPSL en fichiers acceptables par le PCMDI/IPCC. 
  !
  ! Utilisation de la bibliothèque CMOR du PCMDI
  !
  ! Ce programme est appelé avec un argument, le nom du fichier à traiter
  ! Il nécessite aussi un fichier config.def contenant diverses informations 
  ! (voir plus bas) et l'accès à un tableau faisant la correspondance entre 
  ! les noms de variables du modèle et les noms imposés par l'IPCC
  ! Pour l'instant on ne traite que les fichiers contenant la serie 
  ! temporelle d'une seule variable

  ! Date        Programmeur(s)          Historique
  ! ====        ==========              =====================
  ! 2004/08     L. Fairhead             Code original
  ! 2005/01     S. Denvil               Adaptation pour l'axe hybrid sigma alternatif
  !		S. Denvil 		Adaptation pour les variables 2D (lon,lat)
  !		S. Denvil 		Adaptation pour les variables océaniques
  !		S. Denvil 		Adaptation pour l'axe IPCC time1 (pas de bounds)
  !		S. Denvil 		Adaptation pour les variables ISCCP (cldpres et tau)
  !		S. Denvil 		Adaptation pour les variables zonales / f(latitude,depth,region,time)
  ! 2010/05	S. Denvil 		Adaptation pour CMOR2
  ! 2012/06     T. Noel                 Adaptation pour CORDEX
  ! 2016/05	X. JIN                  Adaptation pour Bias-Adjusted CORDEX data
  ! 2016/08     T. Noel                 Adaptation pour Bias-Adjusted (CORDEX and CMIP5 ) in Synda   

  USE cmor_users_functions
  USE netcdf

  IMPLICIT NONE
  !
  CHARACTER (len=45)                              :: first_part, model_id, institute_id, input_institute_id, source, table_entry
  CHARACTER (len=45)                              :: activity,CORDEX_domain,driving_experiment,driving_model_id,driving_model_ensemble_member,driving_experiment_name,rcm_version_id
  CHARACTER (len=60), DIMENSION(1000)             :: ipsl_name, ipsl_units, ipsl_pos, ipcc_name, ipcc_table, ipcc_realm, ipcc_cell
  CHARACTER (len=80)                              :: varname, units, namedim, online_operation, forcing, time_units, time_org_units, input_tracking_id
  CHARACTER (len=128)                             :: inpath, contact, repert, institute, input_institute, calendar, parent_id, parent_rip
  CHARACTER (len=256)                             :: orig_file, expt_id, intifile
  CHARACTER (len=1024)                            :: line_read, comment,refs, second_part
  CHARACTER (len=512)                             :: bc_method, bc_observation, bc_info
  CHARACTER (len=45)                              :: bc_method_id, bc_observation_id, bc_period
  CHARACTER (len=16)                              :: project
  !
  INTEGER, ALLOCATABLE, DIMENSION(:)              :: dimids,axis_ids, axis_ids_final, lendim 
  INTEGER, DIMENSION(5)                           :: start, count 
  INTEGER, DIMENSION(3)                           :: start_ps, count_ps 
  INTEGER, DIMENSION(2)                           :: table_id
  INTEGER                                         :: orig_file_id, orig_file_id_ps, nvars, ndims, action, intifile_id
  INTEGER                                         :: verbos, exit_ctl, indice, index_table
  INTEGER                                         :: realis, initialization, physics, branch_time_int
  INTEGER                                         :: iargc, iostat, ierr, lunout, error_flag
  INTEGER                                         :: i, ilimit, j, iTab, idim, k, v, jmin
  INTEGER                                         :: buffer, nturn, DownBorne, TopBorne, ifactor2D, jfactor2D
  INTEGER                                         :: latid, lonid, timeid
  INTEGER                                         :: varid, varid_ps, varid_bnds, cmorvarid, grid_id
  INTEGER                                         :: xdim, xdim_ordered, ydim, orca_grid_id, XLONG_bounds_id, XLAT_bounds_id, lon_bounds_id, lat_bounds_id
  INTEGER                                         :: ilat, ilon, itime, itim, ilev, vertices
  INTEGER                                         :: i_lat, i_lon
  INTEGER                                         :: time1, time2, days
  INTEGER                                         :: realization, init_method,phy_version, trackingidLength
  !
  LOGICAL                                         :: found, ok_bnds, ok_XLAT, ok_XLONG, stopflag
  LOGICAL                                         :: singleX, singleY, aeroException, oceanException
  LOGICAL                                         :: ok_force_time, ok_force_time_bnds, ok_force_lat_bnds, ok_force_lon_bnds
  LOGICAL                                         :: HasTimeAxis, contfrac, sealevel
  !
  !  uninitialized variables used in communicating with CMOR:
  !  ---------------------------------------------------------
  REAL(kind=8), ALLOCATABLE, DIMENSION(:,:,:,:,:) :: donnees
  REAL(kind=8), ALLOCATABLE, DIMENSION(:)         :: lon, lat
  REAL(kind=8), ALLOCATABLE, DIMENSION(:)         :: x, y,rlon,rlat
  REAL(kind=8), ALLOCATABLE, DIMENSION(:)         :: lon_bounds, lat_bounds
  REAL(kind=8), ALLOCATABLE, DIMENSION(:,:)       :: XLONG, XLAT
  REAL(kind=8), ALLOCATABLE, DIMENSION(:,:)       :: factor2D
  REAL(kind=8), ALLOCATABLE, DIMENSION(:,:,:)     :: XLONG_bounds, XLAT_bounds
  REAL(kind=8), ALLOCATABLE, DIMENSION(:,:,:)     :: XLONG_bounds_tmp, XLAT_bounds_tmp
  REAL(kind=8)                                    :: missing_value, factor, SeaLevelFactor, bufSize
  REAL(kind=8), DIMENSION(12)                     :: deltaTab
  REAL(kind=8), ALLOCATABLE, DIMENSION(:,:)       :: time_bounds
  REAL(kind=8), ALLOCATABLE, DIMENSION(:)         :: time, timetmp, a_coeff, b_coeff
  REAL(kind=8), ALLOCATABLE, DIMENSION(:)         :: a_coeff_bnds, b_coeff_bnds
  REAL(kind=8)                                    :: timeInit, timeDelta, delta, branch_time, a, bmin
  REAL(kind=8), DIMENSION(8)                      :: b
  DOUBLE PRECISION, DIMENSION(2)                  :: pvalues
  
  !
  INTRINSIC iargc
  !
  !--------------------------------------------------------------------------
  ! Initialisations
  lunout                  = 6
  nturn                   = 1
  varname                 = 'xxxxxxxx'
  table_entry             = 'xxxxxxxx'
  found                   = .false.
  HasTimeAxis             = .false.
  ok_bnds                 = .false.
  stopflag                = .false.
  ok_XLAT                 = .false.
  ok_XLONG                = .false.
  singleX                 = .false.
  singleY                 = .false.
  aeroException           = .false.
  oceanException          = .false.
  contfrac                = .false.
  sealevel                = .false.

  ok_force_time           = .false.  ! default .false. read from the data file

  ok_force_time_bnds      = .false.  ! default .true. calculated by the program
  ok_force_lon_bnds       = .false.
  ok_force_lat_bnds       = .false.
  

  !--------------------------------------------------------------------------
  ! On vérifie que l'appel au programme a bien un argument:
  CALL getarg(1, orig_file)
  IF (iargc() == 0 .OR.  orig_file == '-h') THEN
     WRITE(lunout,*)' '
     WRITE(lunout,*)' Utilisation de ce programme: '
     WRITE(lunout,*)' ./ts2IPCC nom_de_fichier [variable]'
     WRITE(lunout,*)'        ou nom_de_fichier est le nom du fichier a traiter'
     WRITE(lunout,*)'        et variable la variable a traiter [optionel]'
     WRITE(lunout,*)' '
     WRITE(lunout,*)' ./ts2IPCC -h sort ce message'
     WRITE(lunout,*)' '
     CALL EXIT(1)
  ENDIF
  IF (iargc() == 2) THEN
     CALL getarg(2, varname)
  ENDIF
  PRINT*, "============================="
  PRINT*, "Input data file:"
  PRINT*, orig_file
  PRINT*, "============================="

  !
  !--------------------------------------------------------------------------
  ! Lecture du fichier de configuration
  OPEN (20, IOSTAT=iostat, file='config.def',form='formatted',status='old')
  IF (iostat /= 0) THEN
     WRITE(lunout,*)'Erreur ouverture du fichier config.def'
     CALL EXIT(1)
  ENDIF
  !
  DO WHILE (iostat == 0)
     READ(20,'(A)',iostat=iostat)line_read
     line_read = TRIM(line_read)
     IF (INDEX(line_read, '#') /= 1) THEN
        first_part = TRIM(line_read(1:INDEX(line_read, '=')-1))
        second_part = TRIM(line_read(INDEX(line_read, '=')+1:))
        SELECTCASE(first_part)

        CASE('inpath')
           inpath = TRIM(second_part)
        CASE('file_action')
           READ(second_part,'(i4)') action
        CASE('verbosity')
           READ(second_part,'(i4)') verbos
        CASE('exit_control')
           READ(second_part,'(i4)') exit_ctl
        CASE('repertoire')
           repert = TRIM(second_part)

        CASE('activity')
           activity = TRIM(second_part)
        CASE('experiment_id')
           expt_id = TRIM(second_part)
        CASE('model_id')
           model_id = TRIM(second_part)
        CASE('contact')
           contact = TRIM(second_part)
        CASE('institute')
           institute = TRIM(second_part)
        CASE('institute_id')
           institute_id = TRIM(second_part)
 

        ! CMIP5 meta-data
        CASE('realization')
           READ(second_part,'(i2)') realis
        CASE('initialization_method')
           READ(second_part,'(i2)') initialization
        CASE('physics_version')
           READ(second_part,'(i2)') physics
        CASE('parent_experiment_id')
           parent_id = TRIM(second_part)
        CASE('parent_experiment_rip')
           parent_rip = TRIM(second_part)  
        CASE('branch_time')
           READ(second_part,'(i5)') branch_time_int

        ! CORDEX meta-data
        CASE('CORDEX_domain')
           CORDEX_domain= TRIM(second_part)
        CASE('driving_model_id')
           driving_model_id = TRIM(second_part)
        CASE('driving_model_ensemble_member')
           driving_model_ensemble_member = TRIM(second_part)
        CASE('driving_experiment_name')
           driving_experiment_name = TRIM(second_part)
        CASE('rcm_version_id')
           rcm_version_id = TRIM(second_part)

       
        ! Biais Adjusted meta-data
        CASE('bc_method')
           bc_method = TRIM(second_part)
        CASE('bc_method_id')
           bc_method_id = TRIM(second_part)
        CASE('bc_observation')
           bc_observation = TRIM(second_part)
        CASE('bc_observation_id')
           bc_observation_id = TRIM(second_part)
        CASE('bc_period')
           bc_period = TRIM(second_part)
        CASE('input_institute')
           input_institute = TRIM(second_part)
        CASE('input_institute_id')
           input_institute_id = TRIM(second_part)
        CASE('input_tracking_id')
           input_tracking_id = TRIM(second_part)

        CASE('source')
           source = TRIM(second_part)
        CASE('forcing')
           forcing = TRIM(second_part)
        CASE('calendar')
           calendar = TRIM(second_part)
        CASE('project')
           project  = TRIM(second_part)
        CASE('comment')
           comment = TRIM(second_part)
        CASE('refs')
           refs = TRIM(second_part)

        CASE('time_units')
           time_units = TRIM(second_part)
        ENDSELECT
     ENDIF
  ENDDO
  IF (iostat > 0) THEN
     WRITE(lunout,*)'Probleme de lecture du fichier config.def, iostat = ',iostat
     CALL EXIT(1)
  ENDIF
  CLOSE(20)

  PRINT*, TRIM(project)//' Adjust project:'
  PRINT*, TRIM(project)//'_grids'

  bc_info=TRIM(bc_method_id)//'-'//TRIM(bc_observation_id)//'-'//TRIM(bc_period)


  !--------------------------------------------------------------------------

  !
  !--------------------------------------------------------------------------
  ! Lecture du tableau de correspondance nom IPSL <=> nom IPCC
  OPEN (20, IOSTAT=iostat, file='./table.def',form='formatted',status='old')
  IF (iostat /= 0) THEN
     WRITE(lunout,*)'Erreur ouverture du fichier table.def'
     CALL EXIT(1)
  ENDIF
  indice = 0
  DO WHILE (iostat == 0)
     READ(20,'(A)',iostat=iostat)line_read
     line_read = TRIM(line_read)
     IF (INDEX(line_read, '#') /= 1) THEN
        indice = indice + 1
        ipsl_name(indice)  = TRIM(ADJUSTL(line_read(1:INDEX(line_read, '|')-1)))
        line_read = TRIM(line_read(INDEX(line_read, '|')+1:))
        !
        ipsl_units(indice) = TRIM(ADJUSTL(line_read(1:INDEX(line_read, '|')-1)))
        line_read = TRIM(line_read(INDEX(line_read, '|')+1:))
        !
        ipsl_pos(indice)   = TRIM(ADJUSTL(line_read(1:INDEX(line_read, '|')-1)))
        line_read = TRIM(line_read(INDEX(line_read, '|')+1:))
        !
        ipcc_name(indice)  = TRIM(ADJUSTL(line_read(1:INDEX(line_read, '|')-1)))
        line_read = TRIM(line_read(INDEX(line_read, '|')+1:))
        !
        ipcc_table(indice) = TRIM(ADJUSTL(line_read(1:INDEX(line_read, '|')-1)))
        line_read = TRIM(line_read(INDEX(line_read, '|')+1:))
        !
        ipcc_realm(indice) = TRIM(ADJUSTL(line_read(1:INDEX(line_read, '|')-1)))
        !
        ipcc_cell(indice)  = TRIM(ADJUSTL(line_read(INDEX(line_read, '|')+1:)))
        !
     ENDIF
  ENDDO
  indice = indice - 1
  CLOSE(20)

  !
  ! Ouverture du fichier a traiter
  ierr = nf90_open(orig_file, NF90_NOWRITE, orig_file_id)
  IF (ierr /= NF90_NOERR) CALL handle_err(ierr)
  !
  ! trouver la variable a traiter, c'est une variable 3 ou 4 dimensions.
  ierr = nf90_inquire(orig_file_id, nVariables=nvars)
  IF (ierr /= NF90_NOERR) CALL handle_err(ierr)
  print*, "nvars =", nvars

  i = 0
  IF (varname == 'xxxxxxxx') THEN
     DO WHILE (.not.found)
        i = i + 1
        IF (i > nvars) THEN
           WRITE(lunout,*)' pas de variable 3d ou 4d trouvee'
           CALL EXIT(1)
        ENDIF

        ierr = nf90_inquire_variable(orig_file_id, i, name=varname)
        IF (ierr /= NF90_NOERR) CALL handle_err(ierr)

        ierr =  nf90_inquire_variable(orig_file_id, i, ndims=ndims)
        IF (ierr /= NF90_NOERR) CALL handle_err(ierr)

        IF (TRIM(ADJUSTL(varname)).EQ.'lon_bnds' ) ok_force_lon_bnds =.FALSE.
        IF (TRIM(ADJUSTL(varname)).EQ.'lat_bnds' ) ok_force_lat_bnds =.FALSE.

        IF (ndims > 2 .AND. TRIM(ADJUSTL(varname)).NE.'lon_bnds'  &
                      .AND. TRIM(ADJUSTL(varname)).NE.'lat_bnds'  &
                      .AND. TRIM(ADJUSTL(varname)).NE.'lon_2'     &
                      .AND. TRIM(ADJUSTL(varname)).NE.'lat_2'     &
           ) found = .true. ! By XiaJIN 18/05/2016
     ENDDO

  ELSE
     ierr = nf90_inq_varid(orig_file_id, varname, varid)
     IF (ierr /= NF90_NOERR) CALL handle_err(ierr)
     print*, "orig_file_id=",orig_file_id," varname=",varname," varid=", varid
  ENDIF

  varname=TRIM(ADJUSTL(varname))

  !
  ! recherche de la correspondance nom IPSL <=> nom IPCC
  found = .false.
  i = 0
  DO WHILE (.not. found)
     i = i + 1
     PRINT*, ' varname = ', TRIM(ADJUSTL(varname)),' ipsl_name(i) = ', TRIM(ADJUSTL(ipsl_name(i)))
     IF (i > indice) THEN
        WRITE(lunout,*)'La variable ',TRIM(varname),' n''est pas dans le tableau de correspondance table.def'
        CALL EXIT(1)
     ENDIF
     IF (TRIM(varname) == TRIM(ipsl_name(i))) THEN
        index_table = i
        found = .true.
     ENDIF
  ENDDO

  PRINT*, 'found a variable to proceed with : '
  PRINT*, '******************************'
  WRITE(lunout,*)'ipsl name      = ', ipsl_name(index_table)
  WRITE(lunout,*)'ipsl units     = ', ipsl_units(index_table)
  WRITE(lunout,*)'ipsl positive  = ', ipsl_pos(index_table)
  WRITE(lunout,*)'cordex name    = ', ipcc_name(index_table)
  WRITE(lunout,*)'cordex table   = ', ipcc_table(index_table)
  WRITE(lunout,*)'cordex realm   = ', ipcc_realm(index_table)
  WRITE(lunout,*)'cordex cell    = ', ipcc_cell(index_table)
  PRINT*, '******************************'
  
  !----------------------------------------------------------------
  !   I. Initialisation CMOR (cmor_setup)
  !----------------------------------------------------------------
  PRINT*, '##########################################'
  PRINT*, 'I. Initialisation CMOR (cmor_setup)'
  PRINT*, '##########################################'

  PRINT*, 'calling cmor_setup '
  ierr = cmor_setup(inpath=inpath,   &
       netcdf_file_action=action,    &
       set_verbosity=verbos,         &
       create_subdirectories=0,      &
       exit_control=exit_ctl)
  PRINT*, 'returned from cmor_setup '
  !
  IF (ierr /= 0) THEN
     WRITE(lunout,*)'Probleme dans cmor_setup, ierr = ', ierr
  ENDIF
  !
  PRINT*, '------------------------------'
  PRINT*, 'calling cmor_load_table ', TRIM(ADJUSTL(ipcc_table(index_table)))
  table_id(1)=cmor_load_table(TRIM(ADJUSTL(ipcc_table(index_table))))
  PRINT*, 'returned from cmor_load_table '

  !----------------------------------------------------------------
  !   . Declarations nouveaux attributs globaux
  !----------------------------------------------------------------
  PRINT*, 'Attributs globaux'

SELECTCASE(project)

        CASE('CORDEX-Adjust')
  error_flag = cmor_set_cur_dataset_attribute("CORDEX_domain",cordex_domain)
  error_flag = cmor_set_cur_dataset_attribute("driving_model_id",driving_model_id)
  error_flag = cmor_set_cur_dataset_attribute("driving_model_ensemble_member",driving_model_ensemble_member)
  error_flag = cmor_set_cur_dataset_attribute("rcm_version_id",rcm_version_id)
       CASE('CMIP5-Adjust')

  ENDSELECT



  error_flag = cmor_set_cur_dataset_attribute("bc_method",bc_method)
  error_flag = cmor_set_cur_dataset_attribute("bc_method_id",bc_method_id)
  error_flag = cmor_set_cur_dataset_attribute("bc_observation",bc_observation)
  error_flag = cmor_set_cur_dataset_attribute("bc_observation_id",bc_observation_id)
  error_flag = cmor_set_cur_dataset_attribute("bc_period",bc_period)
  error_flag = cmor_set_cur_dataset_attribute("bc_info",bc_info)
  error_flag = cmor_set_cur_dataset_attribute("input_tracking_id",TRIM(ADJUSTL(input_tracking_id)))
  error_flag = cmor_set_cur_dataset_attribute("input_institution",input_institute)
  error_flag = cmor_set_cur_dataset_attribute("input_institute_id",input_institute_id)

  branch_time=DBLE(branch_time_int)

 
  !----------------------------------------------------------------
  !   II. Dataset options (cmor_dataset)
  !----------------------------------------------------------------
  PRINT*, '##########################################'
  PRINT*, 'II. Dataset options (cmor_dataset)'
  PRINT*, '##########################################'

  PRINT*, '------------------------------'
  PRINT*, 'calling cmor_dataset'


 SELECTCASE(project)

        CASE('CORDEX-Adjust')
  ierr = cmor_dataset(outpath=TRIM(repert), &
                     experiment_id=expt_id,                &
                     institution=institute,                &
                     source=source,                        &
                     calendar=calendar,                    &
                     realization=realis     ,              &
                     initialization_method=initialization, &
                     physics_version=physics,              &
                     contact=contact,                      &
                     references=refs,                      &
                     model_id=model_id,                    &
                     forcing=forcing,                      &
                     institute_id=institute_id)              
       CASE('CMIP5-Adjust')
  ierr = cmor_dataset(outpath=repert,                       &
       &              experiment_id=expt_id,                &
       &              institution=institute,                &
       &              source=source,                        &
       &              calendar=calendar,                    &
       &              realization=realis,                   &
       &              contact=contact,                      &
       &              comment=comment,                      &
       &              references=refs,                      &
       &              model_id=model_id,                    &
       &              forcing=forcing,                      &
       &              initialization_method=initialization, &
       &              physics_version=physics,              &
       &              institute_id=institute_id,            &
       &              parent_experiment_id=parent_id,       &
       &              branch_time=branch_time,              &
       &              parent_experiment_rip=parent_rip)


ENDSELECT  
         
  PRINT*, 'returned from cmor_dataset '

  IF (ierr /= 0) THEN
     WRITE(lunout,*)'Probleme dans cmor_dataset, ierr = ', ierr
  ENDIF

  !----------------------------------------------------------------
  !   III. Axes and grid definition (cmor_axis and cmor_grid) 
  !----------------------------------------------------------------
  PRINT*, '##########################################'
  PRINT*, 'III. Axes and grid definition (cmor_axis and cmor_grid)'
  PRINT*, '##########################################'

  ! Get number of dimensions for input field
  ierr = nf90_inq_varid(orig_file_id,TRIM(varname), varid)
  IF (ierr /= NF90_NOERR) CALL handle_err(ierr)

  ierr = nf90_Inquire_Variable(orig_file_id, varid, ndims = ndims)
  IF (ierr /= NF90_NOERR) CALL handle_err(ierr)
  print*, 'varname =',trim(varname), 'ndims=', ndims

  ALLOCATE (dimids(ndims))
  ALLOCATE (axis_ids(ndims))
  ALLOCATE (lendim(ndims))

  dimids(:)   = -1000
  axis_ids(:) = -1000
  lendim(:)   = -1000

  ierr = nf90_Inquire_Variable(orig_file_id, varid, dimids = dimids)
  IF (ierr /= NF90_NOERR) CALL handle_err(ierr)
  print*, 'dimids =', dimids

  ! Loop on dimensions
  DO idim = 1, ndims
     ierr = nf90_Inquire_Dimension(orig_file_id, dimids(idim), &
          name = namedim, len = lendim(idim))
     IF (ierr /= NF90_NOERR) CALL handle_err(ierr)
     PRINT*, '------------------------------'
     print*, 'dimids(',idim,') =',dimids(idim)
     print*, 'name =',namedim, ' len =',lendim(idim)
     units=' '
 
     SELECTCASE(TRIM(namedim))
     CASE('lat') ! Atmospheric latitude
                 ! Lecture de la latitude:
        ALLOCATE(lat(lendim(idim)))
        ierr = nf90_inq_varid(orig_file_id, namedim, latid)
        IF (ierr /= NF90_NOERR) CALL handle_err(ierr)
        ierr = nf90_get_var(orig_file_id, latid, lat)
        IF (ierr /= NF90_NOERR) CALL handle_err(ierr)
        ierr = nf90_get_att(orig_file_id, latid, 'units', units)
        IF (ierr /= NF90_NOERR) CALL handle_err(ierr)
        ALLOCATE(lat_bounds(lendim(idim)+1))
        DO i = 2, lendim(idim)
           lat_bounds(i) = lat(i-1) - (lat(i-1) - lat(i))/2.
        ENDDO

        lat_bounds(1) = lat(1)
        lat_bounds(lendim(idim)+1) = lat(lendim(idim))

        !       definition de la latitude
        PRINT*, '------------------------------'
        PRINT*, 'calling cmor_axis latitude atmospheric '
        axis_ids(idim) = cmor_axis(                    &
             table_entry='latitude',                   &
             units= 'degrees',                        &  
             length=lendim(idim),                      &
             coord_vals=lat,                           &
             cell_bounds=lat_bounds)
        ilat=axis_ids(idim)

        PRINT*, 'returned from cmor_axis '

        !
        !
 CASE('lon') ! Atmospheric longitude
                 ! lecture de la longitude:
        ALLOCATE(lon(lendim(idim)))
        ierr = nf90_inq_varid(orig_file_id, namedim, lonid)
        IF (ierr /= NF90_NOERR) CALL handle_err(ierr)
        ierr = nf90_get_var(orig_file_id, lonid, lon)
        IF (ierr /= NF90_NOERR) CALL handle_err(ierr)
        ierr = nf90_get_att(orig_file_id, lonid, 'units', units)
        IF (ierr /= NF90_NOERR) CALL handle_err(ierr)
        ALLOCATE(lon_bounds(lendim(idim)+1))
        DO i = 2, lendim(idim)
           lon_bounds(i) = lon(i-1) - (lon(i-1) - lon(i))/2.
        ENDDO
        lon_bounds(1) = lon(1) - (lon_bounds(3) -lon_bounds(2))/2.
        lon_bounds(lendim(idim)+1) = lon(lendim(idim)) + (lon_bounds(lendim(idim))-lon_bounds(lendim(idim)-1))/2.

        !       definition de la longitude
        PRINT*,'------------------------------'
        PRINT*, 'calling cmor_axis longitude atmospheric '
        axis_ids(idim) = cmor_axis(                    &
             table_entry='longitude',                  &
             units= 'degrees',                        &  
             length=lendim(idim),                      &
             coord_vals=lon,                           &
             cell_bounds=lon_bounds)
        ilon=axis_ids(idim)

        PRINT*, 'returned from cmor_axis '

        !
        !

     CASE('x')       ! lecture de la longitude:
        IF ( lendim(idim).gt.1 ) THEN

           ALLOCATE(x(lendim(idim)))
           x=(/ (i, i=1,lendim(idim)) /)
           xdim=lendim(idim)
           ALLOCATE(rlon(lendim(idim)))

           DO i = 1, lendim(idim)
              rlon(i) = (x(i)-1)*0.11-28.375
              !rlon(i) = (x(i)-1)*0.11-28.375+180.
           ENDDO

           table_id(2)=cmor_load_table(TRIM(project)//'_grids')
           CALL cmor_set_table(table_id=table_id(2))

           !       definition de la longitude
           PRINT*,'------------------------------'
           PRINT*, 'calling cmor_axis longitude'
           axis_ids(idim) = cmor_axis(   &
                table_entry = 'grid_longitude', &
                units = 'degrees',             &
                length = lendim(idim),   &
                coord_vals = rlon )
           i_lon=axis_ids(idim)
           print*, 'axis_ids(',idim,')=',axis_ids(idim)
           print*, 'lendim(',idim,')=',lendim(idim)
           PRINT*, 'returned from cmor_axis '

           ok_XLONG=.true.

           IF ( ok_XLAT ) THEN
              PRINT*, 'We know all we need to call cmor_grid now '
           ENDIF

        ELSE
           singleX=.true.
        ENDIF
        !
        !
     CASE('y')       ! lecture de la latitude:
        IF ( lendim(idim).gt.1 ) THEN

           ALLOCATE(y(lendim(idim)))
           y=(/ (i, i=1,lendim(idim)) /)
           ydim=lendim(idim)
           ALLOCATE(rlat(lendim(idim)))                                                                                 
           DO i = 1, lendim(idim)
              rlat(i)=(y(i)-1)*0.11-23.375
           ENDDO  
           table_id(2)=cmor_load_table(TRIM(project)//'_grids')
           CALL cmor_set_table(table_id=table_id(2))

           !       definition de la latitude
           PRINT*, '------------------------------'
           PRINT*, 'calling cmor_axis latitude '
           axis_ids(idim) = cmor_axis(   &
                table_entry = 'grid_latitude', &
                units = 'degrees',             &
                length = lendim(idim),   &
                coord_vals = rlat)
           i_lat=axis_ids(idim)
           print*, 'axis_ids(',idim,')=',axis_ids(idim)
           print*, 'lendim(',idim,')=',lendim(idim)
           PRINT*, 'returned from cmor_axis '

           ok_XLAT=.true.
           PRINT*, '------------------------------'
!==============================================================================
           IF ( ok_XLAT .AND. ok_XLONG ) THEN
              print *,xdim,ydim
              ALLOCATE(XLONG(xdim, ydim))
              ALLOCATE(XLAT(xdim, ydim))
              
              PRINT*, ' reading lat '
              ierr = nf90_inq_varid(orig_file_id, 'lat', latid)
              IF (ierr /= NF90_NOERR) CALL handle_err(ierr)
              ierr = nf90_get_var(orig_file_id, latid, XLAT)
              IF (ierr /= NF90_NOERR) CALL handle_err(ierr)
              ierr = nf90_get_att(orig_file_id, latid, 'units', units)
              IF (ierr /= NF90_NOERR) CALL handle_err(ierr)

              PRINT*, ' reading lon '
              ierr = nf90_inq_varid(orig_file_id, 'lon', lonid)
              IF (ierr /= NF90_NOERR) CALL handle_err(ierr)
              ierr = nf90_get_var(orig_file_id, lonid, XLONG)
              IF (ierr /= NF90_NOERR) CALL handle_err(ierr)
              ierr = nf90_get_att(orig_file_id, lonid, 'units', units)
              IF (ierr /= NF90_NOERR) CALL handle_err(ierr)


              ! On alloue
              vertices=4

              ALLOCATE (XLAT_bounds(4,xdim, ydim))
              ALLOCATE (XLONG_bounds(4,xdim, ydim))

              IF(ok_force_lat_bnds .AND. ok_force_lon_bnds) THEN
              !----------------------------------------------------------------------------------------------
              DO i = 2, xdim-1
              DO j = 2, ydim-1
              ! DO k = 1, 4

                 XLAT_bounds(1,i,j) = (XLAT(i-1,j-1)+XLAT(i-1,j)+ XLAT(i,j)+ XLAT(i,j-1))/4
                 XLAT_bounds(2,i,j) = (XLAT(i-1,j)+XLAT(i-1,j+1)+ XLAT(i,j+1)+ XLAT(i,j))/4
                 XLAT_bounds(3,i,j) = (XLAT(i,j)+XLAT(i,j+1)+ XLAT(i+1,j+1)+ XLAT(i+1,j))/4
                 XLAT_bounds(4,i,j) = (XLAT(i,j-1)+XLAT(i,j)+ XLAT(i+1,j)+ XLAT(i+1,j-1))/4

                 XLONG_bounds(1,i,j) = (XLONG(i-1,j-1)+XLONG(i-1,j)+ XLONG(i,j)+ XLONG(i,j-1))/4
                 XLONG_bounds(2,i,j) = (XLONG(i-1,j)+XLONG(i-1,j+1)+ XLONG(i,j+1)+ XLONG(i,j))/4
                 XLONG_bounds(3,i,j) = (XLONG(i,j)+XLONG(i,j+1)+ XLONG(i+1,j+1)+ XLONG(i+1,j))/4
                 XLONG_bounds(4,i,j) = (XLONG(i,j-1)+XLONG(i,j)+ XLONG(i+1,j)+ XLONG(i+1,j-1))/4
              !ENDDO
              ENDDO
              ENDDO

              i = 1
              DO j = 2, ydim-1
              ! DO k = 1, 4

                 XLAT_bounds(3,i,j) =  XLAT_bounds(2,i+1,j)
                 XLAT_bounds(4,i,j) =  XLAT_bounds(1,i+1,j)
                 XLAT_bounds(1,i,j) = XLAT_bounds(4,i,j)-(XLAT_bounds(4,i+1,j)-XLAT_bounds(1,i+1,j))
                 XLAT_bounds(2,i,j) = XLAT_bounds(3,i,j)-(XLAT_bounds(3,i+1,j)-XLAT_bounds(2,i+1,j))

                 XLONG_bounds(3,i,j) = XLONG_bounds(2,i+1,j)
                 XLONG_bounds(4,i,j) = XLONG_bounds(1,i+1,j)
                 XLONG_bounds(1,i,j) = XLONG_bounds(4,i,j)-(XLONG_bounds(4,i+1,j)-XLONG_bounds(1,i+1,j))
                 XLONG_bounds(2,i,j) = XLONG_bounds(3,i,j)-(XLONG_bounds(3,i+1,j)-XLONG_bounds(2,i+1,j))
              !ENDDO
              ENDDO
  
              i = xdim
              DO j = 2, ydim-1
              ! DO k = 1, 4

                 XLAT_bounds(1,i,j) =  XLAT_bounds(4,i-1,j)         
                 XLAT_bounds(2,i,j) =  XLAT_bounds(3,i-1,j)          
                 XLAT_bounds(3,i,j) =  XLAT_bounds(2,i,j)+(XLAT_bounds(4,i-1,j)-XLAT_bounds(1,i-1,j))
                 XLAT_bounds(4,i,j) =  XLAT_bounds(1,i,j)+(XLAT_bounds(3,i-1,j)-XLAT_bounds(2,i-1,j))

                 XLONG_bounds(1,i,j) = XLONG_bounds(4,i-1,j)       
                 XLONG_bounds(2,i,j) = XLONG_bounds(3,i-1,j)  
                 XLONG_bounds(3,i,j) = XLONG_bounds(2,i,j)+(XLONG_bounds(4,i-1,j)-XLONG_bounds(1,i-1,j))
                 XLONG_bounds(4,i,j) = XLONG_bounds(1,i,j)+(XLONG_bounds(3,i-1,j)-XLONG_bounds(2,i-1,j))
              !ENDDO
              ENDDO 

              j = 1
              DO i = 1, xdim
              ! DO k = 1, 4

                 XLAT_bounds(2,i,j) = XLAT_bounds(1,i,j+1)
                 XLAT_bounds(3,i,j) = XLAT_bounds(4,i,j+1)
                 XLAT_bounds(1,i,j) = XLAT_bounds(2,i,j)-(XLAT_bounds(2,i,j+1)-XLAT_bounds(1,i,j+1))
                 XLAT_bounds(4,i,j) = XLAT_bounds(3,i,j)-(XLAT_bounds(3,i,j+1)-XLAT_bounds(4,i,j+1))

                 XLONG_bounds(2,i,j) =  XLONG_bounds(1,i,j+1)
                 XLONG_bounds(3,i,j) =  XLONG_bounds(4,i,j+1)
                 XLONG_bounds(1,i,j) =  XLONG_bounds(2,i,j)+(XLONG_bounds(1,i,j+1)-XLONG_bounds(2,i,j+1))
                 XLONG_bounds(4,i,j) =  XLONG_bounds(3,i,j)+(XLONG_bounds(4,i,j+1)-XLONG_bounds(3,i,j+1))

              !ENDDO
              ENDDO

              j = ydim
              DO i = 1, xdim
              ! DO k = 1, 4

                 XLAT_bounds(1,i,j) = XLAT_bounds(2,i,j-1)   
                 XLAT_bounds(4,i,j) = XLAT_bounds(3,i,j-1)
                 XLAT_bounds(2,i,j) = XLAT_bounds(1,i,j)+(XLAT_bounds(2,i,j-1)-XLAT_bounds(1,i,j-1))
                 XLAT_bounds(3,i,j) = XLAT_bounds(4,i,j)+(XLAT_bounds(3,i,j-1)-XLAT_bounds(4,i,j-1))

                 XLONG_bounds(1,i,j) =  XLONG_bounds(2,i,j-1)
                 XLONG_bounds(4,i,j) =  XLONG_bounds(3,i,j-1)
                 XLONG_bounds(2,i,j) =  XLONG_bounds(1,i,j)-(XLONG_bounds(1,i,j-1)-XLONG_bounds(2,i,j-1))
                 XLONG_bounds(3,i,j) =  XLONG_bounds(4,i,j)-(XLONG_bounds(4,i,j-1)-XLONG_bounds(3,i,j-1))

              !ENDDO
              ENDDO
              !----------------------------------------------------------------------------------------------
              ELSE
             
  SELECTCASE(project)

                  CASE('CORDEX-Adjust')
                PRINT*, 'reading lat_counter_bnds'
                 ierr = nf90_inq_varid(orig_file_id, 'lat_vertices', varid_bnds)
                 IF (ierr /= NF90_NOERR) CALL handle_err(ierr)
                 ierr = nf90_get_var(orig_file_id, varid_bnds, XLAT_bounds)
                 IF (ierr /= NF90_NOERR) CALL handle_err(ierr)

                 PRINT*, 'reading lon_counter_bnds'
                 ierr = nf90_inq_varid(orig_file_id, 'lon_vertices', varid_bnds)
                 IF (ierr /= NF90_NOERR) CALL handle_err(ierr)
                 ierr = nf90_get_var(orig_file_id, varid_bnds, XLONG_bounds)
                 IF (ierr /= NF90_NOERR) CALL handle_err(ierr)

        CASE('CMIP5-Adjust')

                 PRINT*, 'reading lat_counter_bnds'
                 ierr = nf90_inq_varid(orig_file_id, 'lat_bnds', varid_bnds)
                 IF (ierr /= NF90_NOERR) CALL handle_err(ierr)
                 ierr = nf90_get_var(orig_file_id, varid_bnds, XLAT_bounds)
                 IF (ierr /= NF90_NOERR) CALL handle_err(ierr)

                 PRINT*, 'reading lon_counter_bnds'
                 ierr = nf90_inq_varid(orig_file_id, 'lon_bnds', varid_bnds)
                 IF (ierr /= NF90_NOERR) CALL handle_err(ierr)
                 ierr = nf90_get_var(orig_file_id, varid_bnds, XLONG_bounds)
                 IF (ierr /= NF90_NOERR) CALL handle_err(ierr)
            ENDSELECT

              ENDIF


              ! Remise en forme des longitudes, cmor2 semble avoir du mal avec cet axe periodique
              WHERE (XLONG.lt.0.)
                 XLONG=360.+XLONG
              ENDWHERE
              !
              ! Remise en forme des bounds longitudes, cmor2 semble avoir du mal avec cet axe periodique
              WHERE (XLONG_bounds.lt.0.)
                 XLONG_bounds=360.+XLONG_bounds
              ENDWHERE
              WHERE (XLONG_bounds.gt.360.)
                 XLONG_bounds=XLONG_bounds-360.
              ENDWHERE
              !

              PRINT*,'------------------------------'
              PRINT*, 'calling cmor_grid from y '
              grid_id = cmor_grid(            &
                   axis_ids = (/ i_lon, i_lat /),   &
                   latitude = XLAT,                 &
                   longitude = XLONG,               &
                   latitude_vertices = XLAT_bounds, &
                   longitude_vertices = XLONG_bounds  &
                   )
              print*, 'grid_id=', grid_id
              print*, 'axis_ids=',i_lon, i_lat                    
              IF (grid_id .GE. 0) CALL handle_err(ierr)

              PRINT*, 'returned from cmor_grid '
           ENDIF

           call cmor_set_table(table_id=table_id(1))

           !---------------------------------------------------------------
           !   .  Mapping Grids 
           !----------------------------------------------------------------
           pvalues(1) = 39.25   ! latitude of new north pole
           pvalues(2) = -162.   ! longitude of new north pole

           PRINT*, 'MAPPING Grids'

           error_flag = cmor_set_grid_mapping(     &
                    grid_id,       &
                    mapping_name="rotated_latitude_longitude",  &
                    parameter_names=(/'grid_north_pole_latitude ','grid_north_pole_longitude'/),  &
                    parameter_values=pvalues,    &
                    parameter_units=(/'degrees_north','degrees_east '/)   &
                    )
           IF (error_flag .NE. 0) CALL handle_err(ierr)
           PRINT*, 'done'

        ELSE
           singleY=.true.
        ENDIF


     CASE('time')
        HasTimeAxis=.true.

        !     definition du temps
        IF (idim /= ndims) THEN
           WRITE(lunout,*)'la dimension temps doit etre la derniere dimension'
           CALL EXIT(1)
        ENDIF

        ALLOCATE(time(lendim(idim)))
        ALLOCATE(timetmp(lendim(idim)))
        ALLOCATE(time_bounds(2,lendim(idim)))

        !
        itime = lendim(idim)
        print*, 'itime =', itime
        print*, 'ipcc_table(index_table) =',ipcc_table(index_table)
        !
        ! Choose between time or time1 (time2 will come sooner or later)
        IF (( index(ipcc_cell(index_table),'time: point',.false.) .eq. 1 )) THEN
           PRINT*,' We have no bounds'
           table_entry='time1'
           ok_bnds=.false.
        ELSEIF ( ipcc_cell(index_table) == 'time: mean within years time: mean over years' ) THEN
           PRINT*,' We have climatic Bounds'
           table_entry='time2'
           ok_bnds=.true.
        ELSE
           PRINT*,' We have regular Bounds'
           table_entry='time'
           ok_bnds=.true.
        ENDIF

        IF (.NOT.ok_force_time) THEN
           ierr = nf90_inq_varid(orig_file_id,namedim,timeid)
           IF (ierr /=0) CALL handle_err(ierr)
           ierr = nf90_get_var(orig_file_id, timeid, time)
           IF (ierr /=0) CALL handle_err(ierr)
           ierr = nf90_get_att(orig_file_id,timeid, 'units', units)
           IF (ierr /=0) CALL handle_err(ierr)

        ELSE
           ! calculate the days between two dates
           ierr = nf90_inq_varid(orig_file_id,namedim,timeid)
           IF (ierr /=0) CALL handle_err(ierr)
           ierr = nf90_get_var(orig_file_id, timeid, timetmp)
           IF (ierr /=0) CALL handle_err(ierr)
           ierr = nf90_get_att(orig_file_id,timeid, 'units', time_org_units)
           !IF (ierr /=0) CALL handle_err(ierr)
           !IF (ierr /=0) units=time_units ! Set a normal value if there is no units in the file
           IF (ierr /=0) time_org_units=time_units ! Set a normal value if there is no units in the file
           PRINT*, "read time units from netcdf file: ", time_org_units

           units="days since 1949-12-01 00:00:00" ! standard units from the table
           IF ( TRIM(ADJUSTL(time_org_units))=="day as %Y%m%d.%f" ) THEN
              time1=19491201
              DO i=1,itime
                 time2=int(timetmp(i))
                 call countdays(time1,time2,days)
                 time(i)=days+(timetmp(i)-int(timetmp(i)))
                 !print*, timetmp(i), days, time(i)
              ENDDO
           ELSE IF ( TRIM(ADJUSTL(time_org_units))=="days since 1949-12-01 00:00:00" ) THEN
              time(:)=timetmp(:)
           ELSE IF ( TRIM(ADJUSTL(time_org_units))=="hours since 1949-12-01 00:00:00" ) THEN
              time(:)=timetmp(:)/24
           ELSE IF ( TRIM(ADJUSTL(time_org_units))=="hours since 1950-01-01 00:00:00" ) THEN
              IF (calendar=="standard" .OR. calendar=="proleptic_gregorian" .OR. calendar=="365_day") THEN
                 time(:)=timetmp(:)/24.+31
              ELSE IF ( calendar=="360_day" ) THEN
                 time(:)=timetmp(:)/24.+30
              ELSE
                 PRINT*,"Lack of calendar information!"
                 call EXIT(1)
              ENDIF
           ELSE IF ( TRIM(ADJUSTL(time_org_units))=="hours since 1951-01-01 00:00:00" ) THEN
              IF (calendar=="standard" .OR. calendar=="proleptic_gregorian" .OR. calendar=="365_day") THEN
                 time(:)=timetmp(:)/24+31+365
              ELSE IF ( calendar=="360_day" ) THEN
                 time(:)=timetmp(:)/24+30+360
              ELSE
                 PRINT*,"Lack of calendar information!"
                 call EXIT(1)
              ENDIF
           ELSE
              PRINT*, "Wrong in calculating time: lack of time units!"
              call EXIT(1)
           ENDIF
           PRINT*, "time_org_units =",TRIM(ADJUSTL(time_org_units)),"; Calendar =",calendar
! delete the wrong time values
           DO i=1,itime
              a=time(i)-int(time(i))
              if( a <= abs(a-0.5) ) a=0.
              if( a >  abs(a-0.5) ) a=0.5
              time(i)=a+int(time(i))
           ENDDO
        ENDIF


        ! On construit les time_bounds
        IF ( (ok_bnds) ) THEN
           IF (ok_force_time_bnds) THEN
              PRINT*, 'computing time_counter_bnds '
!              delta=(time(2)-time(1))
              delta=1.0
              deltaTab(:)=delta/2.
              time_bounds(1,1) = time(1) - deltaTab(1)
              time_bounds(2,1) = time(1) + deltaTab(1)
              !time_bounds(2,1) = time_bounds(1,1) + delta
              PRINT*, time_bounds(1,1), time_bounds(2,1)
              DO i = 2, itime
!                 IF ( MOD(i,12) == 0 ) THEN
!                    iTab=12
!                 ELSE
!                    iTab=MOD(i,12)
!                 ENDIF
!                 IF ((online_operation == 'inst(X)').AND.(ipcc_cell(index_table) == 'time: mean')) THEN
!                    IF (i .eq. 1) PRINT*,'!!!!!!!!!!!!!!!!!!!!!!!!!!!!ERROR!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
!                    IF (i .eq. 1) PRINT*,' Online operation is inst(X) but we force time to be time: mean'
!                    IF (i .eq. 1) PRINT*,'!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
!                    CALL EXIT(1)
!                 ELSE
                    time_bounds(1,i)   = time_bounds(2,i-1)
                    !time_bounds(2,i)   = time(i) + deltaTab(iTab)
                    time_bounds(2,i)   = time_bounds(1,i) + delta
!                 ENDIF
              ENDDO
              PRINT*, ' time_bounds(1,:) = ', time_bounds(1,1:MIN(itime,24))
              PRINT*, ' time_bounds(2,:) = ', time_bounds(2,1:MIN(itime,24))
           ELSE
              PRINT*, ' reading time_counter_bnds '
              ! On lit time_counter_bnds if needed
              ierr = nf90_inq_varid(orig_file_id, 'time_bnds', varid_bnds)
              IF (ierr /= NF90_NOERR) CALL handle_err(ierr)
              ierr = nf90_get_var(orig_file_id, varid_bnds, time_bounds)
              IF (ierr /= NF90_NOERR) CALL handle_err(ierr)
           ENDIF
        ENDIF


        PRINT*,'------------------------------'
        PRINT*, 'calling cmor_axis time '

        axis_ids(idim) = cmor_axis(                 &
             table_entry=TRIM(table_entry),         &
             units=TRIM(units),                     &
             length=lendim(idim),                   &
             interval='')

        PRINT*, 'returned from cmor_axis '
        itim  = axis_ids(idim)
        !
        !
     CASE default
        PRINT*, '******************************'
        WRITE(lunout,*)'Dimension: ', TRIM(namedim),' non reconnue'
        PRINT*, '******************************'
        stopflag=.true.
     ENDSELECT
  ENDDO

  !----------------------------------------------------------------
  !   IV. Variable definition (cmor_variable) 
  !----------------------------------------------------------------
  PRINT*, '##########################################'
  print*," IV. Variable definition (cmor_variable)" 
  PRINT*, '##########################################'

  units=' ' 
  ierr = nf90_inq_varid(orig_file_id,TRIM(varname), varid)
  IF (ierr /= NF90_NOERR) CALL handle_err(ierr)
  print*, 'varname = ', varname

  ierr = nf90_get_att(orig_file_id, varid, 'units', units) 
  IF (ierr /= NF90_NOERR) THEN
     IF ( TRIM(ADJUSTL(varname)) == 'tasAdjust' ) THEN
        units='K'
     ELSE IF ( TRIM(ADJUSTL(varname)) == 'sfcWindAdjust' ) THEN
        units='m s-1'
     ELSE IF ( TRIM(ADJUSTL(varname)) == 'rsdsAdjust' ) THEN
        units='W m-2'
     ELSE IF ( TRIM(ADJUSTL(varname)) == 'prAdjust' ) THEN
        units='kg m-2 s-1'
     ELSE
        CALL handle_err(ierr)
     ENDIF
  ENDIF

  ierr = nf90_get_att(orig_file_id, varid, 'online_operation', online_operation) 
  IF (ierr /= NF90_NOERR) online_operation='N/A'

  ierr = nf90_get_att(orig_file_id, varid, '_FillValue', missing_value)
  IF (ierr /= NF90_NOERR) THEN
     ierr = nf90_get_att(orig_file_id, varid, 'missing_value', missing_value)
     IF (ierr /= NF90_NOERR) THEN
        missing_value=1.0000000E+20
     ENDIF
  ENDIF


  factor=1.

  IF ( ok_XLAT.AND.ok_XLONG ) THEN
     IF (.NOT.oceanException) THEN
        PRINT*,' HERE 1'
        ALLOCATE (axis_ids_final(ndims-1))
        axis_ids_final(1)=grid_id
        DO i=3,ndims
           axis_ids_final(i-1)=axis_ids(i)
        ENDDO
     ELSE
        PRINT*,' HERE 2'
        ALLOCATE (axis_ids_final(ndims-2))
        axis_ids_final(1)=grid_id
        axis_ids_final(2)=axis_ids(4)
     ENDIF     
  ELSEIF (singleX.and.singleY) THEN
     PRINT*,' HERE 3'
     ALLOCATE (axis_ids_final(1))
     axis_ids_final=itim
  ELSEIF (aeroException) THEN
     PRINT*,' HERE 4'
     ALLOCATE (axis_ids_final(ndims+1))
     axis_ids_final(1)=axis_ids(1)
     axis_ids_final(2)=axis_ids(2)
     axis_ids_final(3)=ilev
     axis_ids_final(4)=axis_ids(3)
  ELSE
     PRINT*,' HERE 6'
     PRINT*,'axis_ids_final=axis_ids'
     ALLOCATE (axis_ids_final(ndims))
     axis_ids_final=axis_ids
  ENDIF

  PRINT*,'axis_ids_final: ', axis_ids_final
  PRINT*,'axis_ids: ', axis_ids

  PRINT*,'------------------------------'
  PRINT*, 'calling cmor_variable '
  PRINT*,'varname          = ',TRIM(ipcc_name(index_table))
  PRINT*,'units            = ',TRIM(units)
  PRINT*,'missing_value    = ',missing_value
  PRINT*,'positive         = ',TRIM(ipsl_pos(index_table))
  PRINT*,'original varname = ',TRIM(varname)
  
  cmorvarid = cmor_variable(                        &
       table_entry=TRIM(ipcc_name(index_table)),    &
       units=TRIM(units),                           &
       axis_ids=axis_ids_final,                     &
       missing_value=missing_value,                 &
       positive = TRIM(ipsl_pos(index_table)),      &
       original_name=TRIM(varname))
 ! IF (cmorvarid <= 0) CALL handle_err(cmorvarid)
  PRINT*, 'returned from cmor_variable :', cmorvarid

  !
  ! Lecture de la variable. On va lire la variable pas de temps par pas de temps pour limiter la taille memoire.
  ! (par paquet de 7 Go au lieu de tout charger d'un coup).
  !bufSize=4096.    ! 4G
  bufSize=1028.    ! 1G

  IF ((ndims == 2).AND.(.NOT.HasTimeAxis)) THEN
     PRINT*,'------------------------------'
     PRINT*,'Start reading ', ipsl_name(index_table)
     ALLOCATE (donnees(lendim(1), lendim(2), 1, 1, 1 ))
     ierr = nf90_get_var(orig_file_id, varid, donnees)
     IF (ierr /= NF90_NOERR) CALL handle_err(ierr)
     PRINT*,'Finish reading '

     ! Apply factor due to units problem:
     IF ( factor.ne.1.) THEN
        PRINT*,'Apply this multiplicative factor to data', factor
        WHERE (donnees.ne.missing_value)
           donnees=donnees*factor
        ENDWHERE
     ENDIF

     ! Apply factor due to CONTFRAC problem:
     IF (contfrac) THEN
        PRINT*,'Apply corrective factor for CONTFRAC'
        WHERE (donnees(:,:,1,1,1).ne.missing_value)
           donnees(:,:,1,1,1)=donnees(:,:,1,1,1)/factor2D
        ENDWHERE
     ENDIF

  ELSE IF ((ndims == 2).AND.(HasTimeAxis)) THEN

     buffer = FLOOR( (bufSize * 1024. * 1024.) / (lendim(1) * 4.) )

     ALLOCATE (donnees(lendim(1), MIN(buffer,lendim(2)), 1, 1, 1 ))
     !ALLOCATE (donnees(lendim(1), lendim(2), 1, 1, 1 ))
     nturn  = CEILING(REAL(lendim(2)) / REAL(buffer))

     ! Definition de la portion de variable a lire dans le cas
     ! de series temporelles
     start(1) = 1
     start(2) = 1
     start(3) = 1  ! indice du pas de temps (i, dans ce qui suit)
     start(4) = 1  ! Ne sert a rien dans le cas de ndims == 3
     start(5) = 1  ! Ne sert a rien dans le cas de ndims == 3
     COUNT(1) = lendim(1)             ! station indices
     COUNT(2) = MIN(buffer,lendim(2)) ! pas de temps
     COUNT(3) = 1                     ! Ne sert a rien dans le cas de ndims == 2
     COUNT(4) = 1                     ! Ne sert a rien dans le cas de ndims == 2
     COUNT(5) = 1                     ! Ne sert a rien dans le cas de ndims == 2

  ELSE IF ((ndims == 3).AND.(.NOT.HasTimeAxis)) THEN
     PRINT*,'------------------------------'
     PRINT*,'Start reading ', ipsl_name(index_table)
     ALLOCATE (donnees(lendim(1), lendim(2), lendim(3), 1, 1 ))
     ierr = nf90_get_var(orig_file_id, varid, donnees)
     IF (ierr /= NF90_NOERR) CALL handle_err(ierr)
     PRINT*,'Finish reading '

     ! Apply factor due to units problem:
     if ( factor.ne.1.) THEN
        PRINT*,'Apply this multiplicative factor to data', factor
        WHERE (donnees.ne.missing_value)
           donnees=donnees*factor
        ENDWHERE
     ENDIF

  ELSE IF (ndims == 3) THEN

     buffer = FLOOR( (bufSize * 1024. * 1024.) / (lendim(1) * lendim(2) * 4.) )
     ALLOCATE (donnees(lendim(1), lendim(2), MIN(buffer,lendim(3)), 1, 1 ))
     !ALLOCATE (donnees(lendim(1), lendim(2), lendim(3), 1, 1 ))
     nturn  = CEILING(REAL(lendim(3)) / REAL(buffer))

     ! Definition de la portion de variable a lire dans le cas
     ! de series temporelles
     start(1) = 1
     start(2) = 1
     start(3) = 1  ! indice du pas de temps (i, dans ce qui suit)
     start(4) = 1  ! Ne sert a rien dans le cas de ndims == 3
     start(5) = 1  ! Ne sert a rien dans le cas de ndims == 3
     COUNT(1) = lendim(1)             ! longitudes
     COUNT(2) = lendim(2)             ! latitudes
     COUNT(3) = MIN(buffer,lendim(3)) ! pas de temps
     COUNT(4) = 1                     ! Ne sert a rien dans le cas de ndims == 3
     COUNT(5) = 1                     ! Ne sert a rien dans le cas de ndims == 3
     print*, "Allocate data successfully!!!"

  ELSE IF ((ndims == 4).AND.(oceanException)) THEN

     buffer = FLOOR( (bufSize * 1024. * 1024.) / (lendim(1) * lendim(2) * 4.) )

     ALLOCATE (donnees(lendim(1), lendim(2), 1, MIN(buffer,lendim(4)), 1 ))
     !ALLOCATE (donnees(lendim(1), lendim(2), lendim(3), lendim(4), 1 ))
     nturn  = CEILING(REAL(lendim(4)) / REAL(buffer))

     ! Definition de la portion de variable a lire dans le cas
     ! de series temporelles
     start(1) = 1
     start(2) = 1
     start(3) = 1  ! debut des niveaux verticaux
     start(4) = 1  ! indice du pas de temps (i, dans ce qui suit)
     start(5) = 1  ! Ne sert a rien dans le cas de ndims == 4
     COUNT(1) = lendim(1)             ! longitudes
     COUNT(2) = lendim(2)             ! latitudes
     COUNT(3) = 1                     ! niveaux verticaux
     COUNT(4) = MIN(buffer,lendim(4)) ! pas de temps
     COUNT(5) = 1                     ! Ne sert a rien dans le cas de ndims == 4

  ELSE IF (ndims == 4) THEN

     buffer = FLOOR( (bufSize * 1024. * 1024.) / (lendim(1) * lendim(2) * lendim(3) * 4.) )

     ALLOCATE (donnees(lendim(1), lendim(2), lendim(3), MIN(buffer,lendim(4)), 1 ))
     !ALLOCATE (donnees(lendim(1), lendim(2), lendim(3), lendim(4), 1 ))
     nturn  = CEILING(REAL(lendim(4)) / REAL(buffer))

     ! Definition de la portion de variable a lire dans le cas
     ! de series temporelles
     start(1) = 1
     start(2) = 1
     start(3) = 1  ! debut des niveaux verticaux
     start(4) = 1  ! indice du pas de temps (i, dans ce qui suit)
     start(5) = 1  ! Ne sert a rien dans le cas de ndims == 4
     COUNT(1) = lendim(1)             ! longitudes
     COUNT(2) = lendim(2)             ! latitudes
     COUNT(3) = lendim(3)             ! niveaux verticaux
     COUNT(4) = MIN(buffer,lendim(4)) ! pas de temps
     COUNT(5) = 1                     ! Ne sert a rien dans le cas de ndims == 4

  ELSE IF (ndims == 5) THEN

     buffer = FLOOR( (bufSize * 1024. * 1024.) / (lendim(1) * lendim(2) * lendim(3) * lendim(4) * 4.) )

     ALLOCATE (donnees(lendim(1), lendim(2), lendim(3), lendim(4), MIN(buffer,lendim(5)) ))
     !ALLOCATE (donnees(lendim(1), lendim(2), lendim(3), lendim(4), lendim(5) ))
     nturn  = CEILING(REAL(lendim(5)) / REAL(buffer))

     ! Definition de la portion de variable a lire dans le cas
     ! de series temporelles
     start(1) = 1
     start(2) = 1
     start(3) = 1  ! debut des niveaux verticaux
     start(4) = 1  ! début des niveaux isccp
     start(5) = 1  ! 1 pas de temps
     COUNT(1) = lendim(1)             ! longitudes
     COUNT(2) = lendim(2)             ! latitudes
     COUNT(3) = lendim(3)             ! niveaux verticaux
     COUNT(4) = lendim(4)             ! niveaux isccp
     COUNT(5) = MIN(buffer,lendim(5)) ! pas de temps

  ENDIF

  !
  PRINT*,'------------------------------'
  PRINT*,'Synthese avant ecriture'
  PRINT*,'lendim= ',lendim
  PRINT*,'nturn=  ',nturn

  !----------------------------------------------------------------
  !   V. Variable writing (cmor_write) 
  !----------------------------------------------------------------
   PRINT*, '##########################################'
   print*," V. Variable writing (cmor_write)"
   PRINT*, '##########################################'

  !
  ! Ecriture de la variable
  IF ((ndims == 2).AND.(.NOT.HasTimeAxis)) THEN
     PRINT*,'------------------------------'
     PRINT*, 'calling cmor_write 2D field '
     ierr = cmor_write(                                     &
	var_id        = cmorvarid,                          &
	DATA          = donnees(:,:,1,1,1))

     PRINT*, 'returned from cmor_write '
  ELSE IF ((ndims == 3).AND.(.NOT.HasTimeAxis)) THEN
     PRINT*,'------------------------------'
     PRINT*, 'calling cmor_write 3D field without time axis'
     ierr = cmor_write(                                     &
	var_id        = cmorvarid,                          &
	DATA          = donnees(:,:,:,1,1))

     PRINT*, 'returned from cmor_write '
  ELSE
     DO i = 1, nturn

        ! Lecture des pas de temps dans le cas des series temporelles
        IF (ndims == 2 .OR. ndims == 3 .OR. ndims == 4 .OR. ndims == 5) THEN

           start(ndims) = (i-1) * buffer + 1

           DownBorne=(i-1) * buffer + 1
           TopBorne=min(i * buffer,itime)

           IF (i == nturn) THEN
              buffer=itime-(buffer*(nturn-1))
              count(ndims) = buffer
           ENDIF

           PRINT*,'------------------------------'
           PRINT*,'Start reading ', ipsl_name(index_table)
           !
           ierr = nf90_get_var(orig_file_id, varid, donnees, start, count)
           IF (ierr /= NF90_NOERR) CALL handle_err(ierr)
           !
           WRITE(*,'(" i      = ",i2," /",i2)') i,nturn
           WRITE(lunout,*)'itime  =',itime
           WRITE(lunout,*)'buffer =',buffer
           WRITE(lunout,*)'start  =',start
           WRITE(lunout,*)'count  =',count
           !
           PRINT*,'Finish reading '

           ! Apply factor due to units problem:
           IF ( factor.ne.1.) THEN
              PRINT*,'Apply this multiplicative factor to data', factor
              WHERE (donnees.ne.missing_value)
                 donnees=donnees*factor
              ENDWHERE
           ENDIF
           ! Apply factor due to CONTFRAC problem:
           IF (contfrac) THEN
              PRINT*,'Apply corrective factor for CONTFRAC'
              DO ifactor2D=1,lendim(1)
                 DO jfactor2D=1,lendim(2)
                    WHERE (donnees(ifactor2D,jfactor2D,:,:,:).ne.missing_value)
                       donnees(ifactor2D,jfactor2D,:,:,:)=donnees(ifactor2D,jfactor2D,:,:,:)/factor2D(ifactor2D,jfactor2D)
                    ENDWHERE
                 ENDDO
              ENDDO
           ENDIF
           ! Apply factor to sea level diagnostics:
           ! IPSL-CM5-LR value (from first 100 years of piControl2)
           ! ZOSGA     ZOSSGA ZOSTOGA
           ! -0.08693 -8.572  -8.505
           ! IPSL-CM5-MR value (from first 100 years of piControlMR3)
           ! ZOSGA  ZOSSGA ZOSTOGA
           ! 0.3052 -8.458  -8.403
           IF (sealevel) THEN
              PRINT*,'Apply corrective factor from reference period for sea level diagnostics'
              WHERE (donnees.ne.missing_value)
                 donnees=donnees-SeaLevelFactor
              ENDWHERE
           ENDIF

        ENDIF

        IF (ndims == 2) THEN
           PRINT*,'------------------------------'
           PRINT*, 'calling cmor_write 2D field'

           IF (ok_bnds) THEN
              error_flag = cmor_write(                                &
                   var_id        = cmorvarid,                         &
                   DATA          = donnees(:,:,1,1,1),                &
                   ntimes_passed = buffer,                            &
                   time_vals     = time(DownBorne:TopBorne),          &
                   time_bnds     = time_bounds(:,DownBorne:TopBorne))
              PRINT*, 'returned from cmor_write ok_bnds 1 true'
              IF (error_flag /= 0) stopflag=.true.
           ELSE
              error_flag = cmor_write(                                &
                   var_id        = cmorvarid,                         &
                   DATA          = donnees(:,:,1,1,1),                &
                   ntimes_passed = buffer,                            &
                   time_vals     = time(DownBorne:TopBorne))
              PRINT*, 'returned from cmor_write ok_bnds 2 false'
              IF (error_flag /= 0) stopflag=.true.
           ENDIF

        ELSE IF (ndims == 3) THEN
           PRINT*,'------------------------------'
           PRINT*, 'calling cmor_write 3D field'
           IF (ok_bnds) THEN
              IF (singleX.and.singleY) THEN
                 error_flag = cmor_write(                                &
                      var_id        = cmorvarid,                         &
                      DATA          = donnees(1,1,:,1,1),                &
                      ntimes_passed = buffer,                            &
                      time_vals     = time(DownBorne:TopBorne),          &
                      time_bnds     = time_bounds(:,DownBorne:TopBorne))

                 PRINT*, 'returned from cmor_write ok_bnds 3 true'
                 IF (error_flag /= 0) stopflag=.true.
              ELSE
                 error_flag = cmor_write(                                &
                      var_id        = cmorvarid,                         &
                      DATA          = donnees(:,:,:,1,1),                &
                      ntimes_passed = buffer,                            &
                      time_vals     = time(DownBorne:TopBorne),          &
                      time_bnds     = time_bounds(:,DownBorne:TopBorne))

PRINT*, time(DownBorne:TopBorne)
                 PRINT*, 'returned from cmor_write ok_bnds 4 true'
                 IF (error_flag /= 0) stopflag=.true.
              ENDIF
              !
           ELSE
 print*, "ndims =",ndims, " ok_bnds=",ok_bnds
              error_flag = cmor_write(                                &
                   var_id        = cmorvarid,                         &
                   DATA          = donnees(:,:,:,1,1),                &
                   ntimes_passed = buffer,                            &
                   time_vals     = time(DownBorne:TopBorne))
              PRINT*, 'returned from cmor_write ok_bnds 6 false'
              IF (error_flag /= 0) stopflag=.true.
           ENDIF
        ELSE IF ( (ndims == 4).AND.(oceanException) ) THEN
           PRINT*,'------------------------------'
           PRINT*, 'calling cmor_write 3D field oceanException'
           error_flag = cmor_write(                                &
                var_id        = cmorvarid,                         &
                DATA          = donnees(:,:,1,:,1),                &
                ntimes_passed = buffer,                            &
                time_vals     = time(DownBorne:TopBorne),          &
                time_bnds     = time_bounds(:,DownBorne:TopBorne))

           PRINT*, 'returned from cmor_write 3D field oceanException'
           IF (error_flag /= 0) stopflag=.true.

        ELSE IF (ndims == 4) THEN
           PRINT*,'------------------------------'
           PRINT*, 'calling cmor_write 4D field '
           IF (ok_bnds) THEN
              error_flag = cmor_write(                                &
                   var_id        = cmorvarid,                         &
                   DATA          = donnees(:,:,:,:,1),                &
                   ntimes_passed = buffer,                            &
                   time_vals     = time(DownBorne:TopBorne),          &
                   time_bnds     = time_bounds(:,DownBorne:TopBorne))

              PRINT*, 'returned from cmor_write ok_bnds 7 true'
              IF (error_flag /= 0) stopflag=.true.

           ELSE
              error_flag = cmor_write(                                &
                   var_id        = cmorvarid,                         &
                   DATA          = donnees(:,:,:,:,1),                &
                   ntimes_passed = buffer,                            &
                   time_vals     = time(DownBorne:TopBorne))

              PRINT*, 'returned from cmor_write ok_bnds 8 false'
              IF (error_flag /= 0) stopflag=.true.

           ENDIF
           !

        ELSE IF (ndims == 5) THEN
           PRINT*,'------------------------------'
           PRINT*, 'calling cmor_write 5D field '
           IF (ok_bnds) THEN
              error_flag = cmor_write(                                &
                   var_id        = cmorvarid,                         &
                   DATA          = donnees(:,:,:,:,:),                &
                   ntimes_passed = buffer,                            &
                   time_vals     = time(DownBorne:TopBorne),          &
                   time_bnds     = time_bounds(:,DownBorne:TopBorne))

              PRINT*, 'returned from cmor_write ok_bnds 9 true'
              IF (error_flag /= 0) stopflag=.true.
           ENDIF
        ENDIF
     ENDDO
  ENDIF
  !
  ! Fin CMOR

  PRINT*,'------------------------------'
  PRINT*, 'calling cmor_close '
  PRINT*,'------------------------------'
  error_flag = cmor_close()
  IF (error_flag /= 0) stopflag=.true.
  !
  ! fermeture fichier originel
  ierr = nf90_close(orig_file_id)
  IF (ierr /= NF90_NOERR) CALL handle_err(ierr)

  IF (stopflag) THEN
     WRITE(lunout,*)'Probleme dans cmor_close, ierr = ', error_flag
     PRINT*, '******************************'
     PRINT*, 'CMOR DID NOT COMPLETE '
     PRINT*, '******************************'
     CALL EXIT(1)
  ELSE
     PRINT*, '******************************'
     PRINT*, 'CMOR COMPLETED SUCCESSFULLY '
     PRINT*, '******************************'
     CALL EXIT()
  ENDIF

CONTAINS
!***************************************************************

  SUBROUTINE handle_err(status)
    IMPLICIT NONE
    INTEGER, intent(in) :: status
    WRITE(lunout,*)'Error:',nf90_strerror(status)
    CALL EXIT(1)
  END SUBROUTINE handle_err

!***************************************************************

  SUBROUTINE leap_year(inyear,YNleap)

    IMPLICIT NONE
    integer  , intent(in ) :: inyear
    character, intent(out) :: YNleap

    IF ( mod(inyear,400) .EQ. 0) THEN
       YNleap='Y'
    ELSE IF ( mod(inyear,100) .EQ. 0) THEN
       YNleap='N'
    ELSE IF ( mod(inyear,4) .EQ. 0 ) THEN
       YNleap='Y'
    ELSE
       YNleap='N'
    ENDIF
    !if(YNleap=='Y') print*, inyear
    return
  END SUBROUTINE leap_year

!***************************************************************
  SUBROUTINE countdays(time1,time2,days)
    IMPLICIT NONE
    !REAL(kind=8), intent(in ) :: time1,time2
    integer, intent(in ) :: time1,time2
    integer, intent(out) :: days

    integer, dimension(12) :: monthdays, monthdays_leapyear
    integer :: iyear, iyear1, iyear2, imon, idate
    integer :: days1, days2, days3
    integer :: i, LeapDays
    character :: YNleap

    data monthdays          /31,28,31,30,31,30,31,31,30,31,30,31/
    data monthdays_leapyear /31,29,31,30,31,30,31,31,30,31,30,31/

    days1=0
    days2=0
    days3=0

    print*, time1, time2
! count the days in the first year
    iyear =int(time1/10000)
    imon  =int(mod(time1,10000)/100)
    idate =mod(time1,100)
    !print*, iyear, imon, idate


    call leap_year(iyear,YNleap)
    if (imon==12) then
       days1=31-idate
    else
       if (YNleap=='N') then
          do i=12,imon+1,-1
             days1=days1+monthdays(i)
          end do
          days1=days1+monthdays(imon)-idate
       else
          do i=12,imon+1,-1
             days1=days1+monthdays_leapyear(i)
          end do
          days1=days1+monthdays_leapyear(imon)-idate
       end if
    end if

! count the days in the middle year
    iyear1=int(time1/10000)
    iyear2=int(time2/10000)

    LeapDays=0
    days2=(iyear2-iyear1-1)*365
    do i=iyear1+1,iyear2-1,1
       call leap_year(i,YNleap)
       if(YNleap=='Y') LeapDays=LeapDays+1
    end do
    days2=days2+LeapDays

! count the days in the last year
    iyear =int(time2/10000)
    imon  =int(mod(time2,10000)/100)
    idate =mod(time2,100)
    !print*, iyear, imon, idate

    if (imon==1) then
       days3=idate
    else
       call leap_year(iyear,YNleap)
       if (YNleap=='N') then
          do i=1,imon-1
             days3=days3+monthdays(i)
          end do
       else
          do i=1,imon-1
             days3=days3+monthdays_leapyear(i)
          end do
       end if
       days3=days3+idate
    end if

    days=days1+days2+days3
    !print*,days1,days2,days3
    return
  END SUBROUTINE countdays


!***************************************************************
END PROGRAM standardization
