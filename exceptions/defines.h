#pragma once

#include <iostream>
#include <csetjmp>
#include <vector>

class BaseObject;

const int TRY_BLOCK_COUNT = 10;
std::jmp_buf env[TRY_BLOCK_COUNT];
std::vector<BaseObject *> stacks[TRY_BLOCK_COUNT];

int curr_env = -1;
bool in_clear_stack = false;

class BaseObject {
public:
    BaseObject() {
        printf("BaseObject - Constructor \n");
        stacks[curr_env].push_back(this);
    }

    virtual ~BaseObject() {
        printf("BaseObject - Destructor \n");
    }
};

class SampleObject : public BaseObject {
public:
    SampleObject() {
        printf("SampleObject - Constructor \n");
    }

    ~SampleObject() {
        printf("SampleObject - Destructor \n");
    }
};

#define TRY_BEGIN { \
    ++curr_env; \
    stacks[curr_env].clear(); \
    int exceptionFlag = setjmp(env[curr_env]); \
    switch (exceptionFlag) { \
        case 0:

#define TRY_END \
        break; \
        default: \
        --curr_env; \
        if (curr_env < 0) {printf("Unhandled Exception!"); std::terminate();} \
        std::longjmp(env[curr_env], exceptionFlag); \
    } \
}

#define EXCEPT(exception_flag) \
    break; \
    case exception_flag: \
        --curr_env;


#define RAISE(exception_flag) { \
    in_clear_stack = true;  \
    if (curr_env < 0) {printf("Unhandled Exception!"); std::terminate();} \
    for (int i = stacks[curr_env].size(); i > 0; i--) { \
        BaseObject *obj = stacks[curr_env].back(); \
        stacks[curr_env].pop_back(); \
        delete obj; \
    } \
    in_clear_stack = false; \
    std::longjmp(env[curr_env], exception_flag); \
}

#define BaseException (13)
#define KeyNotFoundError (14)
