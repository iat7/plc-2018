#include <cstdio>

#include "defines.h"

void function() {
    SampleObject another_sample_object = SampleObject();
    RAISE(BaseException);
}

int main() {

    TRY_BEGIN
    {
        TRY_BEGIN
        {
            auto sample_object = SampleObject();
            function();
        };
        EXCEPT(BaseException) {
            printf("Exception - BaseException \n");
            RAISE(BaseException);
        }
        EXCEPT(KeyNotFoundError) {
            printf("Exception - KeyNotFoundError \n");
        }
        TRY_END
    }
    EXCEPT(BaseException)
    {
        printf("Exception - BaseException (from second try_except) \n");
    }
    TRY_END

    TRY_BEGIN
    {
        auto sample_object = SampleObject();
        function();
    };
        EXCEPT(KeyNotFoundError) {
        printf("Exception - KeyNotFoundError");
    }
    TRY_END
}