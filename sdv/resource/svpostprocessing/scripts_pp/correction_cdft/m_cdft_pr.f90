MODULE m_cdft_pr
CONTAINS

subroutine cdftpr(nobs,nref,xobs,xxref,nfut,xxfut,nstep,xcor)
 USE m_sort
 USE IFPORT  

IMPLICIT NONE

! CDFt algorithm for tas-like variables
! *** Assumes no missing data
!         
! Arguments
! nobs  Taille du tableau des observations
! nref  Taille du tableau des données de références
! xobs  Vecteur des observations
! xxref Vecteur des données de références
! nfut  Taille du tableau des données Model
! xxfut Vecteur des données Model
! nstep Nombre de division des cdfs
! cor Vecteur Corrigé (Output)
!
! Date        Programmeur(s)          Historique
! ====        ==========              =====================
!             M. Vrac                 Code original en R
! 2016/01     R. Vautard              Code original en fortran
! 2016/08     T. Noel                 Adaptation et optimisation du programme
!                                     pour l'intégration dans Synda

       INTEGER, parameter :: ndmax=10000
       INTEGER,parameter :: ifl=0
       INTEGER,INTENT(IN) :: nref,nfut,nobs
       REAL,INTENT(INOUT), dimension(nobs) :: xobs
       REAL,INTENT(IN), dimension(nref) :: xxref
       REAL,INTENT(IN), dimension(nfut) :: xxfut
       REAL,INTENT(INOUT), dimension(nfut) :: xcor
       REAL, dimension(nfut) :: xxfuc,xfut20
       INTEGER,INTENT(IN) :: nstep
       REAL, dimension(nfut) :: xfut
       REAL, dimension(nref) :: xref
       integer :: s_ind(5000)


       REAL,dimension(ndmax) :: cdfobs,cdffut2,cdff,x
       INTEGER,dimension(ndmax) :: ind
       
       real :: xrefm,xxmin,xxmax,xobsmin,xrm,xom
       real :: xxmaxE,xxmaxO,xxminE,xxminO

       real :: xfutm,xfut2min,xfut2max,xmi,xma
       real :: temp,xnorm
       real :: qf2r,qo,qf,prob,g
       integer :: nr,nf,i,j,k,l
       integer :: idif,ind1,ind2,icor
       INTEGER :: xit,ind3,iz,iseed

! Initialisation des vecteurs       
xfut(:) = 1.e20
xref(:) = 1.e20
xfut20(:) = 1.e20 


! Normalizing model distrib on obs
! and calculating bounds of distrib
        
       iseed = 765
       iz = 0
       call srand(iseed)

               xrm=-1e12
               xom=-1e12
               
               xrm=maxval(xxref(:))
               xom=maxval(xobs(:))

        
               if(xrm.gt.xom) then
                 xnorm=xom/xrm
               else
                 xnorm=1.
               endif

 !  Desingularization of obs data        
        do xit=1,nobs
            if(xobs(xit).le.1.16e-7) then
                 xobs(xit)=rand(iz)*1.16e-7
             endif
       enddo

 ! normalisation of reference data
        xref(:)=xxref(:)*xnorm

 !  Desingularization  of reference data
        do xit=1,nref
            if(xref(xit).le.1.16e-10) then
                 xref(xit)=rand(iz)*1.16e-10
             endif

       enddo

 ! normalisation of futur data

         xfut(:)=xxfut(:)*xnorm

 !  Desingularization  of futur data
       do xit=1,nfut
              if(xfut(xit).le.1.16e-10) then
                 xfut(xit)=rand(iz)*1.16e-10
             endif
       enddo
       
        
 ! Intitialisation des vecteurs
       xxfuc(:)=1.e20
       xxmax = -1.e20
       xobsmin = 1.e20

! Normalization controls

          xxmaxE = maxval(xref(:))
          xxmaxO = maxval(xobs(:))

          xxmax=max(xxmaxO,xxmaxE)
          xobsmin = minval(xobs(:))

       xfut2min = 1.e20
       xfut2max = -1.e20
       do nf=1,nfut
          ind(nf) = nf
          xfut20(nf) = xfut(nf)
       enddo

          xfut2min = minval(xfut(:))
          xfut2max = maxval(xfut(:))
       
       ! Tri des données 

       call hpsort(nobs,xobs,s_ind)
       call hpsort(nref,xref,s_ind)
       call hpsort(nfut,xfut20,ind)

! Defining sampling marks
! and calculating cdf values

       xmi = 0.
       xma = 2.*xxmax

       do i=1,nstep
          x(i) = xmi +(i-1)*(xma-xmi)/(nstep-1)
          cdfobs(i) = cdf(nobs,xobs,x(i))
          cdffut2(i) = cdf(nfut,xfut20,x(i))


          qf2r = quantile(nref,xref,cdffut2(i))
          cdff(i) = cdf(nobs,xobs,qf2r)
          if(ifl.eq.1)print *,x(i),qf2r,cdfobs(i),cdffut2(i),cdff(i)
       enddo

 !"Left tail"

       if(xobsmin.lt.xfut2min) then
         qo = quantile(nobs,xobs,cdff(1))
         ind1 = 1
         do i=1,nstep
            if(x(i).lt.qo) then
              ind1 = i
            endif
         enddo
         ind2=1
         do i=1,nstep
            if(x(i).lt.xfut2min) then
              ind2 = i
            endif
         enddo
         k = ind1
         j = ind2
         do while (k.gt.0.and.j.gt.0)
            cdff(j) = cdfobs(k)
            k = k - 1
            j = j - 1
         enddo
         do k=1,j
            cdff(k) = 0.
         enddo
       endif

!"Right tail"

       if(cdff(nstep).lt.1.) then
         qf = quantile(nobs,xobs,cdff(nstep))
         i = nstep
         do while (x(i).ge.qf)
            i = i - 1
         enddo
         i = i + 1
         j = nstep - 1
         do while (j.gt.2.and.cdff(j).eq.cdff(nstep))
            j = j - 1
         enddo

!        if(j.eq.0) stop
         idif = min(nstep-j,nstep-i)
         if(ifl.eq.1) print *,i,j,idif
         do k=0,idif
            cdff(j+k) = cdfobs(i+k)
         enddo
         do l=j+idif,nstep
            cdff(l) = 1.
         enddo
       endif

!  Printout for debugging if flag IFL is set to 1
       do i=1,nstep
          if(ifl.eq.1)print *,i,x(i),cdff(i),cdfobs(i)
       enddo


!"Final correction stage: quantile matching of CDF(xfut2) to cdff"
       do nf=1,nfut
          prob = cdf(nfut,xfut20,xfut(nf))
          icor=-1
!  Specific to precipitation
          if(prob.le.cdff(1)) then
            prob=cdff(1)
            icor=0
          endif
          do i=1,nstep-1
         if(cdff(i).lt.cdff(i+1)) then
               if(cdff(i).le.prob.and.cdff(i+1).ge.prob) then
                 g = prob - cdff(i)
                 temp=(1.-g)*x(i) + g*x(i+1)
                 xxfuc(nf)=temp
                 icor=i
             endif
            endif
          enddo
!  Printout for debugging if flag IFL is set to 1
          if(icor.eq.-1) then
            print *,'*** ERROR ICOR=-1 ',prob,cdff(1),cdff(nstep)
            stop
          endif
       enddo
       
             xcor(:)=xxfuc(:)

       return
       
       end subroutine cdftpr

       real function quantile(n,r,p)

! Calculates quantile given data and a probability p
! *** Values of r must be sorted

       real r(n)

       k = int(p*(n-1)) + 1
       g = p*(n-1) - int(p*(n-1))
       if(k.lt.n) then
         quantile = (1.-g)*r(k) + g*r(k+1)
       else
         quantile = r(k)
       endif

       return
       end function quantile

       real function cdf(n,r,z)

!  Calculates CDF function value, input data r(n)
!  r must be sorted

       real r(n)

       if(z.ge.r(n)) then
         cdf = 1.
       else
         cdf = 0.
         do i=1,n-1
            if(r(i).le.z.and.r(i+1).gt.z) then
              cdf = ((i-1)+(z-r(i))/(r(i+1)-r(i)))/(n-1)
              go to 8765
            endif
         enddo
       endif
8765   continue

       return
       end function cdf 


END MODULE m_cdft_pr

