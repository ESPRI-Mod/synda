MODULE m_cdft_tas
CONTAINS

subroutine cdfttas(nobs,nref,xobs,xxref,nfut,xxfut,nstep,xcor)

   USE m_sort
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
! nstep Nombre de division des cdf
! xcor  Vecteur Corrigé (Output)
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
       REAL,INTENT(IN), dimension(nobs) :: xobs
       REAL,INTENT(IN), dimension(nref) :: xxref
       REAL,INTENT(IN), dimension(nfut) :: xxfut
       REAL,INTENT(INOUT), dimension(nfut) :: xcor
       REAL, dimension(nfut) :: xxfuc
       INTEGER,INTENT(IN) :: nstep
       REAL, dimension(nfut) :: xfut20,xfut
       REAL, dimension(nref) :: xref
       integer :: nr,nf,i,j,k,l

       REAL,dimension(ndmax) :: cdfobs,cdffut2,cdff,x
       INTEGER,dimension(nfut) :: ind 
       
       real :: xrefm,xxmin,xxmax,xobsmin,xrm,xom
       real :: xxmaxE,xxmaxO,xxminE,xxminO
       real :: xfutm,xfut2min,xfut2max,xmi,xma
       real :: temp
       real :: qf2r,qo,qf,prob,g
       integer :: idif,ind1,ind2,icor,xit,ind3

!Initialisation des vecteurs
        xfut(:) = 1.e20
        xref(:) = 1.e20
        xfut20(:) = 1.e20 

! Normalizing model distrib on obs
! and calculating bounds of distrib
        
       xrm=SUM(xxref(:))/nref
       xom=SUM(xobs(:))/nobs
       
       ! Normalization
       xref(:)=xxref(:)+xom-xrm
       xfut(:)=xxfut(:)+xom-xrm
              
       xxfuc(:)=1.e20

       xrefm=0.
       xxmin = 1.e20
       xxmax = -1.e20
       xobsmin = 1.e20

! Normalization controls

          xrefm=SUM(xref(:))/nref
          xxminE=minval(xref(:))
          xxmaxE=maxval(xref(:))
       
          xxminO=minval(xobs(:))
          xxmaxO=maxval(xobs(:))
         
          xxmax=max(xxmaxO,xxmaxE)
          xxmin=min(xxminO,xxminE)

          xobsmin=minval(xobs(:))


       xfutm=0.
       xfut2min = 1.e20
       xfut2max = -1.e20

       do nf=1,nfut
          ind(nf) = nf
       enddo


          xfutm=SUM(xfut(:))/nfut

          xfut2min = minval(xfut(:))
          xfut2max = maxval(xfut(:))
          xfut20(:) = xfut(:)
        
 ! Tri des données futur
       call hpsort(nfut,xfut20,ind)

! Defining sampling marks
! and calculating cdf values

       xmi = xxmin-2.*abs(xfutm-xrefm)
       xma = xxmax+2.*abs(xfutm-xrefm)

       do i=1,nstep
          x(i) = xmi +(i-1)*(xma-xmi)/(nstep-1)
          cdfobs(i) = cdf(nobs,xobs,x(i))
          cdffut2(i) = cdf(nfut,xfut20,x(i))
          
          qf2r = quantile(nref,xref,cdffut2(i))
          cdff(i) = cdf(nobs,xobs,qf2r)
          if(ifl.eq.1)print *,x(i),qf2r,cdfobs(i),cdffut2(i),cdff(i)
       enddo



 ! Left tail

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

!  Right tail

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


!  Final correction stage: quantile matching of CDF(xfut2) to cdff
       do nf=1,nfut
          prob = cdf(nfut,xfut20,xfut(nf))
          icor=-1
!  Specific to precipitation
          if(prob.le.cdff(1)) then
            prob=cdff(1)
            icor=0
          endif
          do i=1,nstep-1
               if(cdff(i).le.prob.and.cdff(i+1).ge.prob.and.cdff(i).lt.cdff(i+1)) then
                 g = prob - cdff(i)
                 temp=(1.-g)*x(i) + g*x(i+1)
                 xxfuc(nf)=temp
                 icor=i
               endif
          enddo
!  Printout for debugging if flag IFL is set to 1
          if(icor.eq.-1) then
          print *,'*** ERROR ICOR=-1 ',prob,cdff(1),cdff(nstep)
          stop
          endif
       enddo
       
       
        xcor(:)=xxfuc(:)

       
       end subroutine cdfttas

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


END MODULE m_cdft_tas

