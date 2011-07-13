#include <fitsio.h>
#include <stdio.h>

int main() {
    int status = 0;
    long length;
    fitsfile *fptr;
    fits_open_file(&fptr, "data.fits", READONLY, &status);
    fprintf(stderr, "%s :reading.\n", "test/data.fits");
    fits_movnam_hdu(fptr, BINARY_TBL, "DATA", 0, &status);
    fits_read_key(fptr, TLONG, "NAXIS2", &length , NULL, &status);
    printf("len=%d\n", length);
    double doublenull = 0.;
    int anynul;
    double data[10];
    fits_read_col(fptr, TDOUBLE, 1, 1, 1, 10, &doublenull, data, &anynul, &status);
    int i;
    for (i=0;i<10;i++) {
        printf("%f ",data[i]);
    }
    printf("\n");
    fits_close_file(fptr, &status);
    if (status)          /* print any error messages */
        fits_report_error(stderr, status);
    return(status);
}
