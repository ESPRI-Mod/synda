MODULE m_sort 
CONTAINS

     subroutine HPSORT(N,RA,IND)
IMPLICIT NONE
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

END MODULE m_sort

