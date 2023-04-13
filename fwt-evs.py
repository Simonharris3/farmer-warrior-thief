import copy


class Player:
    choices = []  # how often you choose farmer, warrior, thief
    guesses = []  # how often you guess farmer, warrior, thief as each role

    def __init__(self, choices=None, guesses=None):
        if choices is None:
            choices = [0.06825,  0.3835, 0.54825]
        if guesses is None:
            guesses = [[], [], []]
            guesses[0] = [.9985, 0.0015, 0]
            guesses[1] = [.997125,  0.012875, 0]
            guesses[2] = [0.169125, 0.695125, 0.12575]

        self.choices = choices
        self.guesses = guesses

    def print_strat(self):
        print("Thief percentage: " + str(self.choices[0]))
        print("Farmer percentage: " + str(self.choices[1]))
        print("Warrior percentage: " + str(self.choices[2]) + "\n")

        print("As thief: ")
        print("Guess thief: " + str(self.guesses[0][0]))
        print("Guess farmer: " + str(self.guesses[0][1]))
        print("Guess warrior: " + str(self.guesses[0][2]) + "\n")

        print("As farmer: ")
        print("Guess thief: " + str(self.guesses[1][0]))
        print("Guess farmer: " + str(self.guesses[1][1]))
        print("Guess warrior: " + str(self.guesses[1][2]) + "\n")

        print("As warrior:")
        print("Guess thief: " + str(self.guesses[2][0]))
        print("Guess farmer: " + str(self.guesses[2][1]))
        print("Guess warrior: " + str(self.guesses[2][2]) + "\n")


p1 = Player()
p2 = Player()
p2.choices = [.057, .27475, .66825]
p2.guesses[0] = [.9985, .0015, 0]
p2.guesses[1] = [.9985, .0015, 0]
p2.guesses[2] = [.354875, .444125, .201]


def ev(player=None, strat=None, role=None, role_against=None, change=0.0):
    gu1 = copy.deepcopy(p1.guesses)
    gu2 = copy.deepcopy(p2.guesses)

    ch1 = copy.deepcopy(p1.choices)
    ch2 = copy.deepcopy(p2.choices)

    if player == p1:
        if strat == "choices":
            i_values = increment(ch1[role], ch1[(role + 1) % 3], ch1[(role + 2) % 3], change)
            ch1[role] = i_values[0]
            ch1[(role + 1) % 3] = i_values[1]
            ch1[(role + 2) % 3] = i_values[2]
        if strat == "guesses":
            i_values = increment(gu1[role][role_against], gu1[role][(role_against + 1) % 3],
                                 gu1[role][(role_against + 2) % 3], change)
            gu1[role][role_against] = i_values[0]
            gu1[role][(role_against + 1) % 3] = i_values[1]
            gu1[role][(role_against + 2) % 3] = i_values[2]

    if player == p2:
        if strat == "choices":
            i_values = increment(ch2[role], ch2[(role + 1) % 3], ch2[(role + 2) % 3], change)
            ch2[role] = i_values[0]
            ch2[(role + 1) % 3] = i_values[1]
            ch2[(role + 2) % 3] = i_values[2]
        if strat == "guesses":
            i_values = increment(gu2[role][role_against], gu2[role][(role_against + 1) % 3],
                                 gu2[role][(role_against + 2) % 3], change)
            gu2[role][role_against] = i_values[0]
            gu2[role][(role_against + 1) % 3] = i_values[1]
            gu2[role][(role_against + 2) % 3] = i_values[2]

    tv_t = 2 * (1 - gu2[0][0]) - 2 * (1 - gu1[0][0])
    tv_f = 2 * (1 - gu2[1][0]) - (1 - gu1[0][1]) - gu2[1][0]
    tv_w = 2 * (1 - gu2[2][0]) - 2 * gu2[2][0]

    fv_t = (1 - gu2[0][1]) + gu1[1][0] - 2 * (1 - gu1[1][0])
    fv_f = (1 - gu2[1][1]) + gu1[1][1] - (1 - gu1[1][1]) - gu2[1][1]
    fv_w = (1 - gu2[2][1]) + gu1[1][2] - 2 * gu2[2][1]

    wv_t = 2 * gu1[2][0] - 2 * (1 - gu1[2][0])
    wv_f = 2 * gu1[2][1] - (1 - gu1[2][1]) - gu2[1][2]
    wv_w = 2 * gu1[2][2] - 2 * gu2[2][2]

    t_ev = tv_t * ch2[0] + tv_f * ch2[1] + tv_w * ch2[2]
    f_ev = fv_t * ch2[0] + fv_f * ch2[1] + fv_w * ch2[2]
    w_ev = wv_t * ch2[0] + wv_f * ch2[1] + wv_w * ch2[2]

    # if tv_f != -1*fv_t:
    #     print("ev problem:")
    #     print("tvf: " + str(tv_f))
    #     print("fvt: " + str(fv_t))
    #
    # if wv_t != -1*tv_w:
    #     print("ev problem:")
    #     print("wvt: " + str(wv_t))
    #     print("tvw: " + str(tv_w))
    #
    # if wv_f != -1*fv_w:
    #     print("ev problem:")
    #     print("wvf: " + str(wv_f))
    #     print("fvw: " + str(fv_w))

    return t_ev * ch1[0] + f_ev * ch1[1] + w_ev * ch1[2]


def increment(inc_value, other_a, other_b, incr):

    half_incr = incr / 2.0
    if 0 < inc_value + incr < 1 and 0 < other_a - half_incr < 1 and 0 < other_b - half_incr < 1:
        if inc_value + incr + other_a - half_incr + other_b - half_incr < 0.99 \
                and not inc_value + other_b + other_a < 0.99:
            print("error in case 1")
            original = [inc_value, other_a, other_b]
            print("original values: " + str(original))
            new_vals = [inc_value + incr, other_a - half_incr, other_b - half_incr]
            print("new values: " + str(new_vals))

        return [inc_value + incr, other_a - half_incr, other_b - half_incr]
    elif inc_value + incr >= 1:
        return [1, 0, 0]
    elif other_a - half_incr >= 1:
        return [0, 1, 0]
    elif other_b - half_incr >= 1:
        return [0, 0, 1]
    elif other_a - half_incr <= 0:
        if other_b - half_incr <= 0:
            return [1, 0, 0]
        else:
            diff = incr - other_a
            if inc_value + incr + other_b - diff < 0.99 and not inc_value + other_b + other_a < 0.99:
                print("error in case 2")
            # if 0.99 < inc_value + other_a + other_b < 1.01 and not 0.99 < inc_value+incr + 0 + other_b-diff < 1.01:
            #     print("increment problem:")
            #     print([inc_value, other_a, other_b])
            return [inc_value + incr, 0, other_b - diff]
    elif inc_value + incr <= 0:
        half_value = inc_value / 2.0
        if other_a + half_value + other_b + half_value < 0.99 and not inc_value + other_b + other_a < 0.99:
            print("error in case 3")
        # if 0.99 < inc_value + other_a + other_b < 1.01 and not 0.99 < 0 + other_a+half_value + other_b+half_value <
        # 1.01: print("increment problem:") print([inc_value, other_a, other_b])
        return [0, other_a + half_value, other_b + half_value]
    else:  # other_b - half_incr < 0:
        diff = incr - other_b
        if inc_value + incr + other_a - diff < 0.99 and not inc_value + other_b + other_a < 0.99:
            print("error in case 4")
        return [inc_value + incr, other_a - diff, 0]


print("Starting ev: " + str(ev()))
# print(ev(p1, "guesses", 2, 0, 0.1))

inc = 0.0015

printed_error = False

for i in range(10000):
    if i % 1000 == 0:
        print("loop " + str(i))

    c1 = p1.choices
    g1 = p1.guesses
    c2 = p2.choices
    g2 = p2.guesses

    curr_ev = ev()
    for c in range(len(c1)):
        if ev(p1, "choices", c, None, inc) > curr_ev:
            inc_values = increment(c1[c], c1[(c + 1) % 3], c1[(c + 2) % 3], inc)
            c1[c] = inc_values[0]
            c1[(c + 1) % 3] = inc_values[1]
            c1[(c + 2) % 3] = inc_values[2]

        if ev(p1, "choices", c, None, -1.0 * inc) > curr_ev:
            inc_values = increment(c1[c], c1[(c + 1) % 3], c1[(c + 2) % 3], -1.0 * inc)
            c1[c] = inc_values[0]
            c1[(c + 1) % 3] = inc_values[1]
            c1[(c + 2) % 3] = inc_values[2]

    for g in range(len(g1)):
        for op in range(3):
            if ev(p1, "guesses", g, op, inc) > curr_ev:
                inc_values = increment(g1[g][op], g1[g][(op + 1) % 3], g1[g][(op + 2) % 3], inc)
                g1[g][op] = inc_values[0]
                g1[g][(op + 1) % 3] = inc_values[1]
                g1[g][(op + 2) % 3] = inc_values[2]
            if ev(p1, "guesses", g, op, -1.0 * inc) > curr_ev:
                inc_values = increment(g1[g][op], g1[g][(op + 1) % 3], g1[g][(op + 2) % 3], -1.0 * inc)
                g1[g][op] = inc_values[0]
                g1[g][(op + 1) % 3] = inc_values[1]
                g1[g][(op + 2) % 3] = inc_values[2]

    curr_ev = ev()
    for c in range(len(c2)):
        if ev(p2, "choices", c, None, inc) < curr_ev:
            inc_values = increment(c2[c], c2[(c + 1) % 3], c2[(c + 2) % 3], inc)
            # if c2[0]+c2[1]+c2[2] < 0.9:
            #     bad = True
            c2[c] = inc_values[0]
            c2[(c + 1) % 3] = inc_values[1]
            c2[(c + 2) % 3] = inc_values[2]
            if c2[0]+c2[1]+c2[2] < 0.99 and not printed_error:
                print("changed while incrementing:")
                print("role value: " + str(c))
                print(inc_values)
                printed_error = True
        if ev(p2, "choices", c, None, -1.0 * inc) < curr_ev:
            inc_values = increment(c2[c], c2[(c + 1) % 3], c2[(c + 2) % 3], -1.0 * inc)
            c2[c] = inc_values[0]
            c2[(c + 1) % 3] = inc_values[1]
            c2[(c + 2) % 3] = inc_values[2]
            if c2[0]+c2[1]+c2[2] < 0.99 and not printed_error:
                print("changed while decrementing:")
                print("role value: " + str(c))
                print(inc_values)
                printed_error = True

    for g in range(len(g2)):
        for op in range(3):
            if ev(p2, "guesses", g, op, inc) < curr_ev:
                inc_values = increment(g2[g][op], g2[g][(op + 1) % 3], g2[g][(op + 2) % 3], inc)
                g2[g][op] = inc_values[0]
                g2[g][(op + 1) % 3] = inc_values[1]
                g2[g][(op + 2) % 3] = inc_values[2]
            if ev(p2, "guesses", g, op, -1 * inc) < curr_ev:
                inc_values = increment(g2[g][op], g2[g][(op + 1) % 3], g2[g][(op + 2) % 3], -1 * inc)
                g2[g][op] = inc_values[0]
                g2[g][(op + 1) % 3] = inc_values[1]
                g2[g][(op + 2) % 3] = inc_values[2]

print("Player 1: ")
p1.print_strat()
print("Player 2: ")
p2.print_strat()

print("Final ev: " + str(ev()))
# print("If p1 chose thief less: " + str(ev(p1, "choices", 0, None, -0.3)))
