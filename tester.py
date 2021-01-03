#!python3

import logging, sys
import traceback

log = logging.getLogger("TESTER")
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)


def help():
    log.info("Use the following format to test your homework:")
    log.info("./tester.py 1234567 [-V]")
    log.info("-V or --verbose: Enable verbose logging")
    log.info("Your homework solution is expected to be in the same directory as the tester")


arg_count = len(sys.argv)

log.setLevel(logging.INFO)

if not (1 < arg_count < 4):
    log.critical("Incorrect number of arguments")
    help()
    exit(-1)

if arg_count == 3:
    if sys.argv[2] == "-V" or sys.argv[2] == "--verbose":
        log.setLevel(logging.DEBUG)
    else:
        log.critical("Incorrect optional argument:")
        help()
        exit(-1)

student_number = sys.argv[1]

log.debug("Importing e{}_hw2".format(student_number))

try:
    hw = __import__("e{}_hw2".format(student_number))
except Exception as e:
    log.error(traceback.format_exc())
    log.error("Failed to import e{}_hw2".format(student_number))
    exit(-1)

SampleSet = ("Sample", [
    {
        "KB": ["p(A,f(t))", "q(z)+!p(z,f(B))", "!q(y)+r(y)"],
        "G": ["!r(A)"],
        "R": ('yes', ['p(A,f(t))$q(z)+!p(z,f(B))$q(A)', 'q(A)$!q(y)+r(y)$r(A)', 'r(A)$!r(A)$empty'])
    },
    {
        "KB": ["p(A,f(t))", "q(z)+!p(z,f(B))", "q(y)+r(y)"],
        "G": ["!r(A)"],
        "R": ('no', ['p(A,f(t))$q(z)+!p(z,f(B))$q(A)', 'q(y)+r(y)$!r(A)$q(A)'])
    },
])

SimpleSet = ("Simple", [
    {
        "KB": ["!p(X)", "r(a,Y)+p(b)", "!r(X,b)"],
        "G": ["!r(b,X)"],
        "R": ('yes', ['!p(X)$r(a,Y)+p(b)$r(a,Y)', 'r(a,Y)$!r(X,b)$empty'])
    },
    {
        "KB": ["a(x)", "!a(y)+b(z)", "!b(x)+c(x)"],
        "G": ["!c(A)"],
        "R": ('yes', ['a(x)$!a(y)+b(z)$b(z)', 'b(z)$!b(x)+c(x)$c(x)', 'c(x)$!c(A)$empty'])
    },
    {
        "KB": ["a(A)", "!a(y)+b(y)", "!b(x)+c(x)"],
        "G": ["!c(A)"],
        "R": ('yes', ['a(A)$!a(y)+b(y)$b(A)', 'b(A)$!b(x)+c(x)$c(A)', 'c(A)$!c(A)$empty'])
    },
    {
        "KB": ["a(y)+b(A)", "!a(x)+!b(A)", "a(x)+c(Y)", "!a(x)+b(A)"],
        "G": ["!b(A)"],
        "R": ('yes', ['a(y)+b(A)$!a(x)+b(A)$b(A)', 'b(A)$!a(x)+!b(A)$!a(x)', '!a(x)$a(x)+c(Y)$c(Y)',
                      'b(A)$!b(A)$empty'])
    },
    {
        "KB": ["a(x)+b(y)", "c(x)+a(y)+b(z)", "!c(x)+a(y)+!b(y)"],
        "G": ["!b(A)+!a(B)"],
        "R": ('no', ['a(x)+b(y)$!c(x)+a(y)+!b(y)$a(x)+!c(x)', 'a(x)+!c(x)$!b(A)+!a(B)$!c(B)+!b(A)',
                     '!c(x)+a(y)+!b(y)$!b(A)+!a(B)$!c(x)+!b(B)+!b(A)'])
    },
    {
        "KB": ["human(A)", "!human(A)+!human(b)+likes(A,b)", "!likes(a,B)"],
        "G": ["human(B)"],
        "R": ('yes', ['human(A)$!human(A)+!human(b)+likes(A,b)$!human(b)+likes(A,b)',
                      '!human(b)+likes(A,b)$human(A)$likes(A,A)', '!human(b)+likes(A,b)$!likes(a,B)$!human(B)',
                      '!human(B)$human(B)$empty'])
    },
    {
        "KB": ["hasLotsOfMoney(A)", "!hasLotsOfMoney(a)+!hasPrice(b)+buys(a,b)", "!buys(a,b)+hasPrice(b)", "!buys(A,B)",
               "hasPrice(a)+priceless(a)"],
        "G": ["!priceless(B)"],
        "R": ('yes', ['hasLotsOfMoney(A)$!hasLotsOfMoney(a)+!hasPrice(b)+buys(a,b)$!hasPrice(b)+buys(A,b)',
                      '!hasPrice(b)+buys(A,b)$!buys(A,B)$!hasPrice(B)',
                      '!hasPrice(B)$!buys(a,b)+hasPrice(b)$!buys(a,B)',
                      '!hasPrice(B)$hasPrice(a)+priceless(a)$priceless(B)', 'priceless(B)$!priceless(B)$empty'])
    }
])

UnificationSet = ("Unification", [
    {
        "KB": ["f(g(a),A)+!g(B)", "f(a,A)+!g(b)"],
        "G": ["g(c)"],
        "R": ('no', ['f(g(a),A)+!g(B)$g(c)$f(g(a),A)', 'f(a,A)+!g(b)$g(c)$f(a,A)'])
    },
    {
        "KB": ["f(a)+!g(A)", "!f(A)+!g(a)"],
        "G": ["g(c)"],
        "R": ('yes', ['f(a)+!g(A)$!f(A)+!g(a)$!g(A)', '!g(A)$g(c)$empty'])
    },
    {
        "KB": ["f(u)+!g(u)", "f(A)+g(B)"],
        "G": ["!f(A)"],
        "R": ('no', ['f(u)+!g(u)$f(A)+g(B)$f(B)+f(A)', 'f(B)+f(A)$!f(A)$f(B)', 'f(u)+!g(u)$!f(A)$!g(A)',
                     'f(A)+g(B)$!f(A)$g(B)'])
    },
    {
        "KB": ["f(u)+!g(u)", "f(A)+g(B)"],
        "G": ["!d(A)"],
        "R": ('no', ['f(u)+!g(u)$f(A)+g(B)$f(B)+f(A)'])
    },
    {
        "KB": ["f(u)+g(u)", "!f(x)+g(y)+!f(y)"],
        "G": ["!g(y)"],
        "R": ('yes', ['f(u)+g(u)$!f(x)+g(y)+!f(y)$g(x)+!f(y)', 'g(x)+!f(y)$f(u)+g(u)$g(x)', 'g(x)$!g(y)$empty'])
    },
    {
        "KB": ["f(u)+g(u)", "!f(A)+g(B)+!f(B)"],
        "G": ["!g(B)"],
        "R": ('no', ['f(u)+g(u)$!f(A)+g(B)+!f(B)$g(A)+g(B)+!f(B)', 'g(A)+g(B)+!f(B)$f(u)+g(u)$g(A)+g(B)',
                     'g(A)+g(B)$!g(B)$g(A)', 'f(u)+g(u)$!f(A)+g(B)+!f(B)$g(B)+!f(A)', 'g(B)+!f(A)$!g(B)$!f(A)',
                     'f(u)+g(u)$!g(B)$f(B)', '!f(A)+g(B)+!f(B)$!g(B)$!f(A)+!f(B)'])
    },
])

PropositionalSet = ("Propositional", [
    {
        "KB": ["a+b", "!a+c", "!b+c"],
        "G": ["!c"],
        "R": ('yes', ['a+b$!a+c$b+c', 'b+c$!b+c$c', 'c$!c$empty'])
    },
    {
        "KB": ["p+q", "p+!q", "!p+q"],
        "G": ["!p+!q"],
        "R": ('yes', ['p+q$p+!q$p', 'p$!p+q$q', 'q$!p+!q$!p', '!p$p+!q$!q', '!q$q$empty'])
    }
])

UndefinedBehaviourSet = ("Undefined Behaviour", [
    {
        "KB": ["!a+b", "f(a)", "!g(b)"],
        "G": ["!c"],
        "R": ('no', [])
    },
    {
        "KB": ["f(a+b)+g(u)", "!f(x)"],
        "G": ["!g(A)"],
        "R": ('yes', ['f(a+b)+g(u)$!f(x)$g(u)', 'g(u)$!g(A)$empty'])
    },
    {
        "KB": ["f(!a)+!g(A)", "!f(a)+!g(b)"],
        "G": ["g(c)"],
        "R": ('no', ['f(!a)+!g(A)$g(c)$f(!a)', '!f(a)+!g(b)$g(c)$!f(a)'])
    }
])

ErroneousInputSet = ("Erroneous Input", [
    {
        "KB": ["p(A,f(t))", "q(z)+!p(z,f(B))", "!q(y)+r(y)"],
        "G": ["!!r(A)"],
        "R": (
            'no',
            ['p(A,f(t))$q(z)+!p(z,f(B))$q(A)', 'q(A)$!q(y)+r(y)$r(A)', 'q(z)+!p(z,f(B))$!q(y)+r(y)$!p(y,f(B))+r(y)']
        )
    },
    {
        "KB": ["p(A,,f(t))", "q(z)+!p(z,f(B))", "!q(y)+r(y)"],
        "G": ["!!r(A)"],
        "R": ('no', ['q(z)+!p(z,f(B))$!q(y)+r(y)$!p(y,f(B))+r(y)'])
    },
    {
        "KB": ["p(A,,f(t))", "q(z)+!p(z,f(B)))", "!q(y)+r(y)"],
        "G": ["!!r(A)"],
        "R": ('no', ['q(z)+!p(z,f(B))$!q(y)+r(y)$!p(y,f(B))+r(y)'])
    },
    {
        "KB": ["p(A,f(t))", "q(z)+!p(z,f(B))", "!q(y)++r(y)"],
        "G": ["!r(A)"],
        "R": ('no', ['p(A,f(t))$q(z)+!p(z,f(B))$q(A)'])
    },
])

sets = [SampleSet, SimpleSet, UnificationSet, PropositionalSet, UndefinedBehaviourSet, ErroneousInputSet]

for set in sets:
    fail_count = 0

    for index, test in enumerate(set[1]):
        failed = False

        result = None

        try:
            result = hw.theorem_prover(test["KB"], test["G"])

            if result != test["R"]:
                failed = True
        except Exception as e:
            failed = True
            log.debug(traceback.format_exc())

        if failed:
            fail_count += 1
            log.info("Failed {} {}".format(set[0], index + 1))
            log.debug("Expected: {}".format(test["R"]))
            log.debug("Given: {}".format(result))

    log.info("Passed {}/{} in {} set".format(len(set[1]) - fail_count, len(set[1]), set[0]))
